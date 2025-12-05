import os.path

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
from email.message import EmailMessage

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
GM_CRED_PATH = "./gm_credentials.json"
GM_TOKEN_PATH = "./gm_token.json"

def send(sender, receiver, subject, body):
  creds = get_credentials()
  try:
      service = build("gmail", "v1", credentials=creds)
      message = EmailMessage()

      message.set_content(body)

      message["To"] = receiver
      message["From"] = sender
      message["Subject"] = subject

      # encoded message
      encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

      create_message = {"raw": encoded_message}
      send_message = (
          service.users()
          .messages()
          .send(userId="me", body=create_message)
          .execute()
      )
      print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
      print(f"An error occurred: {error}")
      send_message = None
  return send_message

def get_credentials():
    creds = None
    # The file gm_token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(GM_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(GM_TOKEN_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                GM_CRED_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(GM_TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return creds