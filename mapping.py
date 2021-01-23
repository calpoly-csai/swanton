from fuzzywuzzy import fuzz #added
import stream_deepspeech
from timeit import default_timer as timer

mapper = {
    "swan ton pacific ranch": "Swanton Pacific Ranch",
    "Swanton Pacific Ranch": "Swanton Pacific Ranch",
    "Swanton Pacifico": "Swanton Pacific Ranch",
    "green house" : "Green House",
    "cheese house" : "Cheese House",
    "cause uh very day": "Casa Verde",
    "cause a very day": "Casa Verde",
    "cause a very gay": "Casa Verde",
    "cause very day" : "Casa Verde",
    "as a very dead" : "Casa Verde",
    "Casa Verde": "Casa Verde",
    "romona roderigo" : "Ramon Rodriguez"
}

def get_match(substring):
    keys = [key for key in mapper]
    matches = [(x, fuzz.ratio(substring, x)) for x in keys if fuzz.ratio(substring, x) > 93]
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
    map = mapper
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
            best = best.replace(substring, mapper[match])

    return best

if __name__ == "__main__":

    starttime = timer()
    result = stream_deepspeech.run_stt(10)
    correct = stt_mapper(result)
    print("The time difference is :", timer() - starttime)
    print(correct)
