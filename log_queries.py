import datetime

import pickle

from flask import Flask, request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from os import path, environ

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # Allows read and write access

# Needs to be up here, since we call it on the next line.
def get_spreadsheet_id():
    with open("id.txt") as id_file:
        return id_file.readline()

# The ID, range, and auth path for appending to the spreadsheet.
SPREADSHEET_ID = environ.get("SPREADSHEET_ID", get_spreadsheet_id())
RANGE_NAME = 'A1'  # Should always place the new query correctly at the bottom of the table
AUTH_PATH = 'credentials.json'

BAD_REQUEST = 400
SUCCESS = 200
SERVER_ERROR = 500

app = Flask(__name__)

def config_api():
    """
    Configures the Google Sheets API service to be used for appending data

    :return: The service as a Resource object, or None if there is no pickle and the authentication JSON can't be found
    """

    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(AUTH_PATH, SCOPES)
            except FileNotFoundError as e:
                print(e)
                return None
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)


def log_query(service, question: str, answer: str, sentiment: str = "N/A", spreadsheet_id: str = SPREADSHEET_ID) -> int:
    """
    Logs a user query and chat bot response to a Google Sheet as well as the timestamp

    :param service: Google Sheets API service
    :param question: User question
    :param answer: Chat bot answer
    :param sentiment: Positive or negative sentiment associated with the question/answer, currently defaults to "N/A"
    :param spreadsheet_id: ID of the spreadsheet to append to, currently defaults to an empty string
    :return: 0 on success, 1 on failure
    """

    timestamp = str(datetime.datetime.now())
    values = [[question, answer, sentiment, timestamp]]
    body = {
        'values': values
    }

    try:
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()
    except Exception as e:
        print(e)
        return 1

    return 0

@app.route("/query", methods=["POST"])
def log_route():
    request_body = request.get_json()
    question = request_body.get("question")
    answer = request_body.get("answer")
    sentiment = request_body.get("sentiment")
    if question is None or answer is None or sentiment is None:
        return "Request was missing a required parameter", BAD_REQUEST
    if(log_query(config_api(), question, answer, sentiment) == 0):
        return "Success", SUCCESS
    else:
        return "Failed to log the query", SERVER_ERROR


if __name__ == "__main__":
    app.run(host="0.0.0.0")
