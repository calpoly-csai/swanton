from fuzzywuzzy import fuzz #added
import stream_deepspeech
from timeit import default_timer as timer
import json

mapper = {
    "swan ton pacific ranch": "Swanton Pacific Ranch",
    "Swanton Pacific Ranch": "Swanton Pacific Ranch",
    "Swanton Pacifico": "Swanton Pacific Ranch",
}

with open("test_json.json", "w") as in_json:
    json.dump(mapper, in_json)

def get_match(substring):
    """Returns the best match of a given substring, otherwise, returns no match"""
    keys = [key for key in mapper]
    matches = [(x, fuzz.ratio(substring, x)) for x in keys if fuzz.ratio(substring, x) > 70]
    ordered = sorted(matches, key=lambda x: x[1], reverse=True) #orders
    if len(ordered) > 0:
        return ordered[0][0] #get the best match
    else:
        return "no match"

def get_all_substrings(string):
    """Returns a list of n-size substrings from a given string where n is from 1 to number of words in the string"""
    string_list = string.split()
    combinations = [" ".join(string_list[i:j])
                    for i in range(len(string_list))
                    for j in range (i+1, len(string_list)+ 1)]
    return combinations


def stt_mapper(result):
    """Returns the corrected result"""
    best = result

    replaced = False
    map = mapper
    for key in map: #check if it matches what we have already
        if key in result:
            best = result.replace(key, map[key])
            replaced = True
    if replaced == True:
        return best

    variations = get_all_substrings(result)
    for substring in variations:
        match = get_match(substring)
        if match != "no match": #there was a match
            best = best.replace(substring, mapper[match])

    return best

""" NOT OPTIMAL 
def get_consecutive_variations(string): #Too many for loops
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
"""

if __name__ == "__main__":

    starttime = timer()
    result = stream_deepspeech.run_stt(10)
    correct = stt_mapper(result)
    print("The time difference is :", timer() - starttime)
    print(correct)
