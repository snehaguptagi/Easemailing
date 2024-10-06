import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_credentials(creds_path='credentials.json', token_path='token.json'):
    """
    Authenticate and return Gmail API credentials.
    
    Args:
        creds_path (str): Path to the credentials file.
        token_path (str): Path to the token file.
        
    Returns:
        creds (google.oauth2.credentials.Credentials): The authenticated credentials object.
    """
    creds = None
    try:
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                creds = flow.run_local_server(port=0)

            with open(token_path, 'w') as token:
                token.write(creds.to_json())

    except FileNotFoundError:
        print(f"The file '{creds_path}' was not found. Please check the path and try again.")
    except json.JSONDecodeError:
        print(f"Error decoding '{creds_path}'. Please check the file format.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return creds

if __name__ == '__main__':
    creds = get_credentials()
    if creds:
        print("Credentials successfully obtained.")
    else:
        print("Failed to obtain credentials.")
