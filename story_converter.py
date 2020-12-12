import argparse
import csv
import sys
import re

def main() -> None:
    '''
    Parses through the command-line arguments, reading in the path to the
    stories & generic utterances/intents CSV.
    '''
    
    parser = argparse.ArgumentParser(
        description='Converts the stories and generic CSVs to a file\
             format required for Rasa training')
    parser.add_argument(
        '--stories', 
        dest="stories",
        help='Chatbot story CSV', 
        required=True)
    parser.add_argument(
        '--generic', 
        dest="generic",
        help='Generic Utterances & Intents CSV', 
        required=True)
    args = parser.parse_args()

    story_dat = read_csv(args.stories)[0]
    gen_dat, fields = read_csv(args.generic)   

    gen_dict = create_generic(fields, gen_dat)

    story_str, intents, utterances = generate_stories(story_dat, gen_dict) 
    nlu_str = generate_nlu(intents, gen_dict)
    domain_str = generate_domain(intents, utterances)

    store_file(story_str, "stories.md")
    store_file(nlu_str, "nlu.md")
    store_file(domain_str, "domain.yml")

def store_file(
                file_str:str,
                file_path:str) -> None:
    '''
    Take the string and store it in the file path.

    :param file_str: The data to be stored in the file path.
    :param file_path: The file path that stores file_str.

    '''

    with open(file_path, "w") as open_file:
        open_file.write(file_str)

    print("Data has been stored in %s" % file_path)

def generate_domain(
                        intents:dict,
                        utterances:dict) -> str: 
    '''
    Iterate through the intents & utter dicts and produce the domain.md string

    :param intents: dictionary of the intents.
    :param intents: dictionary of the utterances.

    :returns domain_str: string of domain.yaml 
    '''

    domain_str = "intents:\n"
    template_str = "\nresponses:\n"

    for intent in intents.keys():
        domain_str += ("  - %s\n" % intent)
        
    domain_str += "\nactions:\n"

    for utter in utterances.keys():
        domain_str += ("  - %s\n" % utter)
        template_str += ("  %s:\n" % utter)
        template_str += ("  - text: \"%s\"\n\n" % utterances[utter])

    domain_str += template_str

    return domain_str

def generate_nlu(
                    intents:dict,
                    gen_dict: dict) -> str: 
    '''
    Iterate through the intents dict and produce the nlu.md string

    :param intents:     dictionary of the intents.
    :param gen_dict:    dictionary of the generic data.

    :returns nlu_str: string of the nlu.md 
    '''

    nlu_str = ""

    for intent in intents.keys():
        if(intents[intent] != set()):
            
            nlu_str += ("## intent:%s\n" % intent)

            for example in intents[intent]:
                nlu_str += ("- %s\n" % example)
            
            nlu_str += "\n"

    for gen in gen_dict.keys():
        nlu_str += ("## intent:%s\n" % gen)

        for gen_dat in gen_dict[gen]:
            nlu_str += ("- %s\n" % gen_dat)
        nlu_str += "\n"

    return nlu_str
    
def create_generic(
                    fields:list,
                    generic:list) -> dict:
    '''
    Parses through the generic data rows and creates the list of generic
    responses.

    Example:
    gen_dict = {
                "REJECT" : [
                                "No thank you.",
                                "Nope.",
                                "I am not interested.",
                                "No thanks.",
                                "No.",
                                "Nah."
                            ]
    }
    :param fields: list of strs that are the fields of the CSV data
    :param generic: list of str lists that represent each row of the generic
                    data CSV

    :returns gen_dict: dictionary of the generic data
    '''

    gen_dict = {}
    dict_index = {}

    # Add fields with empty lists to the dict
    for i, field in enumerate(fields):
        gen_dict[field] = []
        dict_index[str(i)] = field

    # Add each generic sample to the dictionary
    for row in generic:
        for i, col in enumerate(row):
            if (col != ''):
                gen_dict[dict_index[str(i)]].append(col)

    return gen_dict

def generate_stories(
                        stories:list,
                        gen_dict:dict) -> tuple: 
    '''
    Parses the list of stories and creates the markdown files.

    :param stories: list of string lists which is each row of the stories CSV.
    :param gen_dict: dictionary of the generic label and its data as a list of 
                     strings.

    :returns story_str: string of the story.md 
    :returns intents: dict of the intent and its examples
    :returns utterances: dict of the utterance and its raw string
    '''

    intents = {}
    utterances = {}
    story_str = ""
    path_name = ""

    for story_row in stories:
        story_type = story_row[0]
        story_dets = story_row[1:]
        
        if (story_type == "PATH"):
            path_name = story_dets[0]
            story_str += "## %s\n" % story_dets[0]

        elif (story_type == "INTENT"):
            if (story_dets[0] in gen_dict):
                story_str += ("* %s\n" % story_dets[0])
                intents[story_dets[0]] = set()
            else:
                curr_intent = story_dets[0].replace(" ", "_")

                story_str += ("* %s\n" % curr_intent)

                if (curr_intent not in intents):
                    intents[curr_intent] = set()

                for story_det in story_dets:
                    if (story_det != ''):
                        intents[curr_intent].add(story_det)

        elif (story_type == "UTTER"):
            curr_utter = "utter_%s" % story_dets[0].replace(" ", "_")
            story_str += ("  - %s\n" % curr_utter)
            utterances[curr_utter] = story_dets[0]

        elif ((story_type == "GENERIC") or (story_type == "GENNAME")):
            print("Generic utterance... skipping...")

        elif (story_type == ''):
            story_str += "\n"
            print("Empty row... Skipping...")

        else:
            print("Error: Invalid story type of %s" % story_type)
            exit()

    return story_str, intents, utterances

def read_csv(csv_path: str) -> list:
    '''
    Reads the CSV row-by-row and each column in a list.
    An example is as follows:

    csv_contents = [
        [
            "Yes",
            "No thank you",
            "Have a great day"
        ],
        [
            "I would like to know.",
            "Nope.",
            "Good bye!"
        ]
    ]

    :param csv_path: Path to the QA pairs CSV
    :returns csv_contents: A list of string lists which are each row of the CSV.
    '''
    csv_contents = []

    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        csvreader = csv.reader(csv_file)

        fields = next(csvreader)

        for row in csvreader:
            row_dat = []

            for col in row:
                row_dat.append(col)

            csv_contents.append(row_dat)

    return csv_contents, fields

if __name__ == "__main__":
    main()