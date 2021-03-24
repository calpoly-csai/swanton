from fuzzywuzzy import fuzz #added
import stream_deepspeech
from timeit import default_timer as timer
import json

stopwords = ["did", "how", "get", "is", "to", "the", "what", "a", "about", "do"] #need to load stopwords into a hashtable or a list

mapper = {
    "swan ton pacific ranch": "Swanton Pacific Ranch",
    "Swanton Pacific Ranch": "Swanton Pacific Ranch",
    "Swanton Pacifico": "Swanton Pacific Ranch",
    "Swanton" : "Swanton Pacific Ranch",
    "Swanton Pacific": "Swanton Pacific Ranch"
}

with open("test_json.json", "w") as in_json:
    json.dump(mapper, in_json)

def get_match(substring):
    """Returns the best match of a given substring, otherwise, returns no match"""
    keys = [key for key in mapper]
    matches = [(mapper[x], fuzz.ratio(substring, x)) for x in keys if fuzz.ratio(substring, x) > 70]
    ordered = sorted(matches, key=lambda x: x[1], reverse=True) #orders by the best matches
    if len(ordered) > 0:
        return ordered[0][0] #get the best match
    else:
        return "no match"

def get_substrings(string):
    """Returns a list of n-size substrings from a given string where n is from 1 to number of words in the string"""
    string_list = string.split()
    combinations = [string_list[i:j]
                    for i in range(len(string_list))
                    for j in range (i+1, len(string_list)+ 1)]
    return combinations

def filter_stopwords(combinations):
    """Filters out substrings with stopwords"""
    filtered = []
    for substring in combinations:
        append = True
        for word in substring:
            if word in stopwords:
                append = False
        if append == True:
            filtered.append(substring)
    return filtered

def generate_n_grams(list):
    """Prioritizes larger substrings over smaller substrings"""
    list.sort(key=len, reverse=True)
    concatenated = [" ".join(substring) for substring in list] #concatenated the words within the substrings cuz they were in lists before
    return concatenated

def stt_mapper(result):
    """Returns the corrected text"""
    best = result

    variations = filter_stopwords(get_substrings(result))
    n_grams = generate_n_grams(variations)
    print(n_grams)
    changed = []
    for substring in n_grams:
        no_change = False
        for phrase in changed: #checks if a particular phrase has already been changed
            if substring in phrase:
                no_change = True
        match = get_match(substring)
        if match != "no match" and no_change == False: #there was a match
            best = best.replace(substring, match)
            changed.append(substring)

    return best

""" might remove later
    replaced = False
    map = mapper
    for key in map: #check if it matches what we have already
        if key in result:
            best = result.replace(key, map[key])
            replaced = True
    if replaced == True:
        return best """

if __name__ == "__main__":

    starttime = timer()
    result = stream_deepspeech.run_stt(5)
    correct = stt_mapper(result)
    print("The time difference is :", timer() - starttime)
    print(correct)
