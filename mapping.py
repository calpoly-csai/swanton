from fuzzywuzzy import fuzz #added
import stream_deepspeech
from timeit import default_timer as timer
import json

def get_match(substring):
    """Returns the best match of a given substring, otherwise, returns no match"""
    matches = [(correctionJSON()[key], fuzz.ratio(substring, key)) for key in correctionJSON().keys()
               if fuzz.ratio(substring, key) > 70]
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
            if word in listing_stopwords("stopwords.txt"):
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

def listing_stopwords(filename):
    """Returns a list of all the stopwords in stopwords.txt"""
    try:
        h = open(filename)
    except:
        raise FileNotFoundError
    h.close()
    f = open(filename, 'r')
    list = []
    lines = f.readlines()
    for line in range(len(lines)):  # each line has one word
        list.append(lines[line].strip())
    f.close()
    """Improvement could be where we load the stopwords into a hash table"""
    return list

def correctionJSON():
    """Returns the JSON object containing corrected names"""

    """Reads from corrections.json"""
    myjsonfile = open('corrections.json')
    jsondata = myjsonfile.read()

    """Parsing"""
    object = json.loads(jsondata)
    return object

if __name__ == "__main__":

    starttime = timer()
    result = stream_deepspeech.run_stt(4)
    correct = stt_mapper(result)
    print("The time difference is :", timer() - starttime)
    print(correct)
