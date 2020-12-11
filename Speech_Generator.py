import argparse
import csv
import json
import numpy as np
import os
from pydub import AudioSegment
import sys
import time
import wave

from google.cloud import texttospeech

disallowed_set = {
                    "PATH",
                    "INTENT",
                    "",
                    "GENERIC",
                    "GENNAME"
                 }

class Audio_Data_Gen:
    
    def __init__(self, credentials:str="auth.json", 
                 accent:str="US", 
                 speaker:str="D") -> None:

        self.accent = accent
        self.speaker = speaker

        data_dir_name = "response_data"

        # get path for credentials
        self.credential_path = credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credential_path

        # instantiate GCP TTS objects
        self.tts_client = texttospeech.TextToSpeechClient()

        # contains the chunks of streamed data
        self.frames = []

        # Path to the response data
        self.data_dir_path = os.path.join(os.getcwd(), data_dir_name)

        # Creates data path if DNE
        if (not(os.path.isdir(self.data_dir_path))):
            os.makedirs(self.data_dir_path)

        self.file_mapping = {
            "<<GENERICS>>":set()
        }

    def parse_rows(self, paths:list) -> set:
        '''
        Takes multiple CSVs, reads each row-by-row, and stores the answers 
        as a dict. Updates the file mapping dict on generic data
        An example is as follows:

        answers_set = {
            "Sorry, I do not know the answer to your question.",
            "The ranch is 3200 acres.",
            "Fred Swanton"
        }

        :param paths: List of paths to the data CSVs
        :returns answers_set: Answer string within the set
        '''

        answers_set = {
            "Sorry, I do not know the answer to your question."
        }

        for path in paths:
            rows = self.read_csv(path)
            generic_name = ""

            for row in rows:
                # Extract the cell from the 2nd column
                answer = row[1]

                if (row[0] not in disallowed_set):

                    # Add to set if it is not in the set
                    if (answer not in answers_set):
                        answers_set.add(answer)

                elif (row[0] == "GENNAME"):
                    generic_name = row[1]
                    self.file_mapping["<<GEN>>%s" % generic_name] = []
                    self.file_mapping["<<GENERICS>>"].add(generic_name)

                elif (row[0] == "GENERIC"):
                    if (answer not in answers_set):
                        answers_set.add(answer)

                    self.file_mapping["<<GEN>>%s" % generic_name].append(answer)

        return answers_set

    def read_csv(self, csv_path: str) -> list:
        '''
        Reads the CSV row-by-row and stores the rows as a list of strs. 

        :param csv_path: Path to the QA pairs CSV
        :returns rows: List of strs of each row of a CSV
        '''
        rows = []

        # Open the CSV
        with open(csv_path, 'r') as csv_file:

            # Instantiate CSV object based on input CSV
            csvreader = csv.reader(csv_file)

            # Remove the CSV header
            fields = next(csvreader)

            # Iterate through each row
            for row in csvreader:
                rows.append(row)

        return rows

    def Text_To_Speech(self, csv_paths:list) -> None:
        '''
        Iterates through the set of answer strings and generates audio of the 
        string which is stored with a corresponding JSON file to map audio
        files to the answer string. 

        :param csv_path: Paths to the QA pairs CSVs
        :returns N/A
        '''

        gen_name = ""

        sample_count = 0

        dataset = self.parse_rows(csv_paths)

        for answer_str in dataset:
            if answer_str not in self.file_mapping["<<GENERICS>>"]:
                # Build the voice request, select the language code 
                # ("en-US") and the ssml voice gender ("neutral")
                voice = texttospeech.VoiceSelectionParams(
                    language_code='en-%s' % self.accent,
                    name='en-%s-WaveNet-%s' % (self.accent, self.speaker))

                # Select the type of audio file you want returned
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                    sample_rate_hertz=16000)

                # Set the text input to be synthesized
                synthesis_input = texttospeech.SynthesisInput(text=answer_str)
                
                # Perform the text-to-speech request on the text input with 
                # the selected voice parameters and audio file type
                answer_audio = self.tts_client.synthesize_speech(
                    input=synthesis_input, 
                    voice=voice, 
                    audio_config=audio_config)

                self.store_data(
                    answer_str, 
                    answer_audio, 
                    sample_count)

                sample_count += 1
    
    def store_data(self, 
        answer_str:str, 
        answer_audio:list, 
        sample_count:int) -> None:
        '''
        Takes the answer str, the audio of the str, and the current file number
        and stores the audio & JSON

        :param answer_str: string containing the current answer
        :param answer_audio: audio byte array of the synthesized string
        :param sample_count: integer count of the current file # 
        '''

        file_name = "response_%s.wav" % str(sample_count)
        file_path = os.path.join(self.data_dir_path, file_name)

        with open(file_path, 'wb') as out:
            out.write(answer_audio.audio_content)

        sound = AudioSegment.from_wav(file_path)
        sound = sound.set_channels(1)
        sound.export(file_path, format="wav")

        print("Audio String: %s => File Written: %s" % (answer_str, file_name))

        self.file_mapping[answer_str] = file_name
        self.file_mapping["<<GENERICS>>"] = list(self.file_mapping["<<GENERICS>>"])
        json_path = os.path.join(self.data_dir_path, "answer_to_file.json")
        with open(json_path, "w") as outfile: 
            json.dump(self.file_mapping, outfile, indent=3) 

if __name__ == "__main__":     
    parser = argparse.ArgumentParser(
        description='Generates audio responses for the answers of the\
             QA pairs CSV')
    parser.add_argument(
        '--json', 
        dest="json",
        help='Authentication JSON', 
        required=True)
    parser.add_argument(
        '--csv', 
        dest="csv",
        help='QA Pairs CSV', 
        nargs="+",
        type=str,
        required=True)
    parser.add_argument('--accent',
        dest="accent",
        help='Accent of the speaker',
        default="US")
    parser.add_argument('--speaker',
        dest="speaker",
        help='Speaker voice (US: A - F | UK: A - F | AU: A - D)',
        default="D")
    args = parser.parse_args()  

    data_gen = Audio_Data_Gen(args.json,
                              args.accent,
                              args.speaker)
    data_gen.Text_To_Speech(args.csv)