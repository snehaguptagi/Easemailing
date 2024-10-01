{
  "installed": {
    "client_id": "YOUR_CLIENT_ID",
    "project_id": "YOUR_PROJECT_ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": [
      "http://localhost"
    ]
  }
}
try:
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
except FileNotFoundError:
    print("The file 'credentials.json' was not found.")
except json.JSONDecodeError:
    print("Error decoding 'credentials.json'. Please check the file format.")
except Exception as e:
    print(f"An error occurred: {e}")
from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_credentials():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    return creds

if __name__ == '__main__':
    get_credentials()
