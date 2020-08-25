import csv
from typing import Dict

def log_to_csv(input: Dict) -> None:
    '''
    - Opens a CSV in this directory
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
    filename = './temp_log.csv'

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(input.keys())
        writer.writerow(input.values())