from deepspeech import Model, version
import numpy as np
import pyaudio
import sys
from fuzzywuzzy import fuzz #added
import mapping
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
    print("Listening...")
    # Record audio and run inference on audio buffers
    while(timer() - stream_start < time_len):
        buff = np.frombuffer(i_stream.read(CHUNK), dtype=np.int16)
        stream.feedAudioContent(buff)
        
    print("Finished...")
    # Close the stream and call PyAudio destructor
    i_stream.stop_stream()
    i_stream.close()
    p.terminate()

    # Obtain the model prediction
    result = stream.finishStream()

    result = "What is swanton pacifico rancho used for"
    # Output the prediction
    print("result: ", stt_mapper(result))


    return result


def get_match(substring):
    keys = [key for key in mapping.mapper]
    matches = [(x, fuzz.ratio(substring, x)) for x in keys if fuzz.ratio(substring, x) > 85]
    ordered = sorted(matches, key=lambda x: x[1], reverse=True) #orders
    if len(ordered) > 0:
        return ordered[0][0] #get the best match
    else:
        return "no match"

def get_consecutive_variations(string):
    variations = []
    array = string.split()
    for i in range(len(array)): #loop through every substring
        end = len(array[i + 1:len(array)]) #number of substrings from the current substring to the last substring
        string = array[i]  #initialize the string to be the current word
        pos = i + 1 #next string position
        variations.append(string) #append the first word
        while end > 0:
            new = string + " " + array[pos] #combine the string with the next substring
            variations.append(new) #append it as a variation
            string = new #set the string as the newly combined string
            pos += 1 #set the position to be the next substring
            end -= 1 #subtract the number of substrings left to account for by 1
    return variations

def stt_mapper(result):
    best = result

    replaced = False
    map = mapping.mapper
    for key in map: #check if it matches what we have already
        if key in result:
            best = result.replace(key, map[key])
            replaced = True
    if replaced == True:
        return best

    variations = get_consecutive_variations(result)
    for substring in variations:
        match = get_match(substring)
        if match != "no match": #there was a match
            print(substring)
            best = best.replace(substring, mapping.map(match))

    return best
"""
    for token in result.split(): #loops through every individual token
    matches = get_match(token, list)
    if len(matches) > 0: #there is a match
        match = matches[0][0] #grab the first match
        best = best.replace(token, match) #replace the token with the best match
"""



if __name__ == "__main__":
    if (len(sys.argv) != 2):
        sys.exit("Usage: python stream_deepspeech.py {stream time}")

    elif (not((sys.argv[1]).isdigit())):
        sys.exit("Argument 'stream time' must be of type 'int'")

    starttime = timer()
    run_stt(int(sys.argv[1]))
    print("The time difference is :", timer() - starttime)