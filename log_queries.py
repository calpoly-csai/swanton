import datetime

import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # Allows read and write access

# The ID, range, and auth path for appending to the spreadsheet.
SPREADSHEET_ID = '15f_zVJxNnUz_9G5ZYPery68rR8PyUnO0yWKSyGQjy4w'
RANGE_NAME = 'A1'  # Should always place the new query correctly at the bottom of the table
AUTH_PATH = 'credentials.json'


def config_api():
    """
    Configures the Google Sheets API service to be used for appending data

    :return: The service as a Resource object
    """

    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                AUTH_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)


def log_query(service, question: str, answer: str) -> None:
    """
    Logs a user query and chat bot response to a Google Sheet as well as the timestamp

    :param service: Google Sheets API service
    :param question: User question
    :param answer: Chat bot answer
    :return: None
    """

    timestamp = str(datetime.datetime.now())
    values = [[question, answer, timestamp]]
    body = {
        'values': values
    }

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()
