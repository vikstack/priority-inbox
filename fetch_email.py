import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]



def get_emails():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        results = service.users().messages().list(userId="me", maxResults=10).execute()
        messages = results.get("messages", [])

        emails = []
        for msg in messages:
            # in this line we define what to fetch from the gmail api,
            #  in this case we want to fetch the subject and the sender of the email 
            message = service.users().messages().get(userId="me", id=msg["id"], format="metadata",
                                                      metadataHeaders=["Subject", "From"]).execute()
            headers = message["payload"]["headers"]
            subject = ""
            sender = ""
            for header in headers:
                if header["name"] == "Subject":
                    subject = header["value"]
                if header["name"] == "From":
                    sender = header["value"]
            emails.append(f"Subject: {subject} From: {sender}")        
            #print("---")
        #for email in emails:
         #   print(email)
        emails = list(dict.fromkeys(emails))      

        return emails
        #return emails        

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    get_emails()