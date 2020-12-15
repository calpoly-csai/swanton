import json
import os
import pyaudio
import random
import sys
import time
import wave

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
DEFAULT_PATH = os.path.join(os.getcwd(), "response_data")

def audio_response(
                    file_map:dict,
                    response_str:str,
                    response_dir:str=DEFAULT_PATH) -> None:
    """
    Takes the string response, maps the response to a file name, and outputs
    the audio from the file name.

    :param file_map: dict with responses as keys and audio file names as values
    :param response_str: string of the predicted response
    :param response_dir: string of the path to the response data
    """

    pa_o = pyaudio.PyAudio()
    ostream = pa_o.open(
        format = FORMAT, 
        channels = CHANNELS, 
        rate = RATE, 
        output = True, 
        frames_per_buffer = CHUNK)

    if (response_str in file_map["<<GENERICS>>"]):
        ran_resp = random.choice(file_map["<<GEN>>%s" % response_str])
        file_name = file_map[ran_resp]

    elif (response_str not in file_map):
        file_name = file_map["Sorry, I do not know "\
        "the answer to your question."]

    else:
        file_name = file_map[response_str]

    file_path = os.path.join(response_dir, file_name)

    if (os.path.exists(file_path) == False):
        raise Exception("Path %s does not exist." % file_path)

    else:
        wf = wave.open(file_path, 'rb')
        
    print("\"%s\" maps to \"%s\"" % (response_str, file_name))
    print("Playing file => \"%s\"" % file_path)

    ostream.write(wf.readframes(wf.getnframes()))

    time.sleep(1)

if __name__ == "__main__":
    response_path = os.path.join(os.getcwd(), "response_data")
    response_json = os.path.join(response_path, "answer_to_file.json")

    with open(response_json, "r") as in_json:
        file_map = json.load(in_json)

    audio_response(file_map, sys.argv[1], response_path)
