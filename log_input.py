import csv, os
from typing import Dict

def log_to_csv(input: Dict) -> None:
    '''
    - Opens a CSV in this directory (will create one if it doesn't exist)
    - Stores the log with the columns for the row in the same order as the dict 
        (question, answer, time, score)
    - Closes the CSV

    Paramters:
        - input: Dict = {
            "question": "User input string [string]",
            "answer": "Predicted answer [string]",
            "time": "Current time [HH:MM:SS] (PST) and date [MM:DD:YYYY]",
            "score": "Confidence score of the input [float]"
        }
    '''
    filepath = './temp_log.csv'
    already_exists = os.path.exists(filepath)

    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if not already_exists:
            writer.writerow(input.keys())
        writer.writerow(input.values())