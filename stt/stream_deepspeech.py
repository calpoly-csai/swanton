from deepspeech import Model, version
import wave
import pyaudio
import numpy as np
from timeit import default_timer as timer

# Audio constants
CHUNK = 2048  # Buffer size
FORMAT = pyaudio.paInt16  # Sample Size
CHANNELS = 1  # Sample Depth
RATE = 16000  # Sample Rate

# Timer length
TIME_LEN = 5

def run_stt(time_len=TIME_LEN):

    # Audio buffer
    frames = []

    # Instantiate Pyaudio
    p = pyaudio.PyAudio()

    # Instantiate Deepspeech
    ds = Model("deepspeech-0.8.1-models.pbmm")
    ds.enableExternalScorer("deepspeech-0.8.1-models.scorer")

    # Get the model sample rate
    desired_sample_rate = ds.sampleRate()

    # Start Deepspeech inference stream
    stream = ds.createStream()

    # Start stream timer
    stream_start = timer()

    # Open the audio stream
    i_stream = p.open(format=FORMAT, channels=CHANNELS, rate=desired_sample_rate,
                                input=True, output=True, frames_per_buffer=CHUNK)

    # Record audio and run inference on audio buffers
    while(timer() - stream_start < time_len):
        buff = np.frombuffer(i_stream.read(CHUNK), dtype=np.int16)
        stream.feedAudioContent(buff)

    # Close the stream and call PyAudio destructor
    i_stream.stop_stream()
    i_stream.close()
    p.terminate()

    # Obtain the model prediction
    result = stream.finishStream()

    # Output the prediction
    print("result: ", result)

    return result

if __name__ == "__main__":
    run_stt(5)