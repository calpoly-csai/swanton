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
        '--utter', 
        dest="utter",
        help='Utterances CSV', 
        required=True)
    parser.add_argument(
        '--intent', 
        dest="intent",
        help='Intents CSV', 
        required=True)        
    args = parser.parse_args()

    story_dat, _ = read_csv(args.stories)
    intent_dat, fields = read_csv(args.intent)   
    utter_dat, _ = read_csv(args.utter)   

    gen_dict = create_generic(fields, intent_dat, utter_dat)

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

    with open(file_path, "w", encoding='utf-8') as open_file:
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

    print(utterances)

    for utter in utterances.keys():
        domain_str += ("  - %s\n" % utter)

        template_str += ("  %s:\n" % utter)

        for utter_sample in utterances[utter]:            
            utter_norm = utter_sample.replace("\"", "\'")
            template_str += ("  - text: \"%s\"\n" % utter_sample)
        template_str += "\n"

    domain_str += template_str
    domain_str += "session_config:\n"
    domain_str += "  session_expiration_time: 60\n"
    domain_str += "  carry_over_slots_to_new_session: true\n"
    
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
        if gen in intents:
            nlu_str += ("## intent:%s\n" % gen)

            for gen_dat in gen_dict[gen]:
                nlu_str += ("- %s\n" % gen_dat)
            nlu_str += "\n"

    return nlu_str

def parse_utter(utter_dat:list) -> dict:
    '''
    Parses through the utterance data and stores them into a dict.

    :param utter_dat: list of the rows from the generic utterance CSV
    :return gen_dat: dict of utterances
    
    '''
    generic_name = ""
    gen_dat = {}

    for row in utter_dat:

        if (row[0] == "GENNAME"):
            generic_name = row[1]
            gen_dat[generic_name] = []

        elif (row[0] == "GENERIC"):
            if (generic_name not in gen_dat):
                print("Error: %s has not been defined." % generic_name)

            else:
                gen_dat[generic_name].append(row[1])

        elif (row[0] == ""):
            pass

        else:
            print("Error: Invalid format of %s in utterance dataset." % row[0])
            exit()

    return gen_dat

def create_generic(
                    fields:list,
                    intent_dat:list,
                    utter_dat:list) -> dict:
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
    :param intent_dat: list of str lists that represent each row of the intent
                    data CSV
    :param utter_dat: list of str lists that represent each row of the utter
                    data CSV

    :returns gen_dict: dictionary of the generic data
    '''

    gen_dict = parse_utter(utter_dat)
    dict_index = {}

    # Add fields with empty lists to the dict
    for i, field in enumerate(fields):
        gen_dict[field] = []
        dict_index[str(i)] = field

    # Add each generic sample to the dictionary
    for row in intent_dat:
        for i, col in enumerate(row):
            if (col != ''):
                gen_dict[dict_index[str(i)]].append(col)

    print(gen_dict)
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

    print("gen dict", gen_dict)

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
                curr_intent = re.sub(r'[^\w\s]','',story_dets[0]) 
                curr_intent = curr_intent.replace(" ", "_")

                story_str += ("* %s\n" % curr_intent)

                if (curr_intent not in intents):
                    intents[curr_intent] = set()

                for story_det in story_dets:
                    if (story_det != ''):
                        intents[curr_intent].add(story_det)

        elif (story_type == "UTTER"):
            curr_utter = re.sub(r'[^\w\s]','',story_dets[0]) 
            curr_utter = "utter_%s" % curr_utter.replace(" ", "_")
            story_str += ("  - %s\n" % curr_utter)

            if story_dets[0] in gen_dict:
                utterances[curr_utter] = gen_dict[story_dets[0]]

            else: 
                utterances[curr_utter] = [story_dets[0]]

        elif ((story_type == "GENERIC") or (story_type == "GENNAME")):
            print("Generic utterance... skipping...")

        elif (story_type == ''):
            story_str += "\n"
            print("Empty row... Skipping...")

        else:
            print("Error: Invalid story type of %s" % story_type)
            exit()

    # print(utterances)

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