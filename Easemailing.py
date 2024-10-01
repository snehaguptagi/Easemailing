from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

def get_gmail_service():
    """Create and return the Gmail API service."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                logging.error(f"Error refreshing token: {e}")
                return None
        else:
            logging.error("Credentials are not valid. Please re-authenticate.")
            return None
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        logging.error(f"Error initializing Gmail service: {e}")
        return None

