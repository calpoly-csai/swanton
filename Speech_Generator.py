import csv
import io
import json
import numpy as np
import os
import pyaudio
from pydub import AudioSegment
import subprocess
import sys
import time
import wave

from google.cloud import texttospeech

class Audio_Data_Gen:
    
    def __init__(self, credentials="auth.json"):
       
        # audio input parameters
        self.CHUNK = 2048
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.RECORD_SECONDS = 5

        data_dir_name = "response_data"

        # get path for credentials
        self.credential_path = credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credential_path

        # pyaudio i/o object instantiation
        self.pa_o = pyaudio.PyAudio()

        # instantiate GCP TTS objects
        self.tts_client = texttospeech.TextToSpeechClient()

        self.file_name = os.path.join(
                os.path.dirname(__file__),
                'resources',
                'audio.raw')

        # open an output audio data stream
        self.ostream = self.pa_o.open(
            format = self.FORMAT, 
            channels = self.CHANNELS, 
            rate = 24000, 
            output = True, 
            frames_per_buffer = self.CHUNK)

        # contains the chunks of streamed data
        self.frames = []

        self.data_dir_path = os.path.join(os.getcwd(), data_dir_name)

        if (not(os.path.isdir(self.data_dir_path))):
            os.makedirs(self.data_dir_path)

    def read_csv(self, csv_path: str) -> dict:
        '''
        Reads the CSV row-by-row and stores the answers as a set. 
        An example is as follows:

        answers_set = {
            "The ranch is 3200 acres.",
            "Fred Swanton"
        }

        :param csv_path: Path to the QA pairs CSV
        :returns answers_set: Answer string within the set
        '''

        with open(csv_path, 'r') as csv_file:
            answers_set = set()
            csvreader = csv.reader(csv_file)

            fields = next(csvreader)

            for row in csvreader:
                answer = row[1]
                if (answer not in answers_set):
                    answers_set.add(answer)

        return answers_set

    def Text_To_Speech(self, csv_path):
        '''
        Iterates through the set of answer strings and generates audio of the 
        string which is stored with a corresponding JSON file to map audio
        files to the answer string. 

        :param csv_path: Path to the QA pairs CSV
        :returns N/A
        '''

        sample_count = 0
        self.file_mapping = {}

        dataset = self.read_csv(csv_path)
        for answer_str in dataset:

            speaker_accent = "US" #"GB"
            speaker = "D"

            # Build the voice request, select the language code 
            # ("en-US") and the ssml voice gender ("neutral")
            voice = texttospeech.VoiceSelectionParams(
                language_code='en-%s' % speaker_accent,
                name='en-%s-WaveNet-%s' % (speaker_accent, speaker))

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
    
    def store_data(self, answer_str, answer_audio, sample_count):
        '''
        Takes the answer str, the audio of the str, and the current file number
        and stores the audio & JSON

        :param answer_str: string containing the current answer
        :param answer_audio: audio byte array of the synthesized string
        :param sample_count: integer count of the current file # 
        '''

        file_name = "speech_sample_%s.wav" % str(sample_count)

        file_path = os.path.join(self.data_dir_path, file_name)

        print("Audio String: %s => File Written: %s" % (answer_str, file_name))
        with open(file_path, 'wb') as out:
            out.write(answer_audio.audio_content)

        sound = AudioSegment.from_wav(file_path)
        sound = sound.set_channels(1)
        sound.export(file_path, format="wav")
        
        self.file_mapping[answer_str] = file_name

        json_path = os.path.join(self.data_dir_path, "answer_to_file.json")
        with open(json_path, "w") as outfile: 
            json.dump(self.file_mapping, outfile, indent=3) 

if __name__ == "__main__":       
    if (len(sys.argv) != 3) or \
    (sys.argv[1][-4:] != ".csv") or \
    (sys.argv[2][-5:] != ".json"):
        sys.exit("Usage: python Speech_Generator.py /path/to/qa.csv"\
                 " /path/to/auth.json")

    data_gen = Audio_Data_Gen(sys.argv[2])
    data_gen.Text_To_Speech(sys.argv[1])