import json
import numpy as np
import os
import pyaudio
import wave

from aiy.board import Board, Led
from deepspeech import Model, version
from timeit import default_timer as timer

import audio_response
import rasa_api_call

MODEL_NAME = "deepspeech-0.8.1-models.tflite"
MODEL_SCORER = "deepspeech-0.8.1-models.scorer"

CHUNK = 2048  # Buffer size
FORMAT = pyaudio.paInt16  # Sample Size
CHANNELS = 1  # Sample Depth

record_bool = True

def end_record():
    """
    Callback function to start and stop the audio recordings

    """

    global record_bool
    print("released...")
    record_bool = False

def load_data(response_path:str) -> tuple:
    """
    Loads the response audio mapper and Deepspeech model data

    :param response_path: path to the response dir with speech response data
    :return file_map: dict with intent str as key and file name str as value
    :return ds: Deepspeech object with loaded model 
    """
    response_json = os.path.join(response_path, "answer_to_file.json")

    with open(response_json, "r") as in_json:
        file_map = json.load(in_json)
    
    ds = Model(MODEL_NAME)
    ds.enableExternalScorer(MODEL_SCORER)

    return file_map, ds

def main():
    """
    Main function that waits for the button press and predicts on audio stream
    data until the button is released. The question is sent to the local Rasa
    server and the response intent is mapped to the appropriate audio file 
    which is output. 
    
    """
    global record_bool
    
    response_path = os.path.join(os.getcwd(), "response_data")

    file_map, ds = load_data(response_path)

    desired_sample_rate = ds.sampleRate()

    with Board() as board:
        board.button.when_released = end_record

        while(True):
            print("Waiting...")
            board.button.wait_for_press()

            record_bool = True
            frames = []

            stream = ds.createStream()
            p = pyaudio.PyAudio()

            i_stream = p.open(format=FORMAT, channels=CHANNELS, rate=desired_sample_rate,
                                        input=True, output=True, frames_per_buffer=CHUNK)

            board.led.state = Led.ON

            while(record_bool):
                print("Recording...")
                buff = np.frombuffer(i_stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
                stream.feedAudioContent(buff)

            board.led.state = Led.OFF

            buff = np.frombuffer(i_stream.read(2 * CHUNK), dtype=np.int16)
            stream.feedAudioContent(buff)

            i_stream.stop_stream()
            i_stream.close()
            p.terminate()

            result = stream.finishStream()

            print("result: ", result)
            intent = rasa_api_call.get_intent(result)
            audio_response.audio_response(file_map, intent, response_path)
                
            p.terminate()

if __name__ == "__main__":
    main()
