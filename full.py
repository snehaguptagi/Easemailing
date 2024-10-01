from __future__ import print_function
import os.path
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from transformers import pipeline
from cryptography.fernet import Fernet
import plotly.express as px
import pandas as pd
import argparse
from flask import Flask, request, jsonify

# Gmail API setup
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def send_email(service, to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {
        'raw': encoded_message
    }

    send_message = service.users().messages().send(userId="me", body=create_message).execute()
    print(f'Sent email to {to}')

# Agents
class EmailCompositionAgent:
    def run(self, subject, body, recipients, attachments=None):
        email = {
            "subject": subject,
            "body": body,
            "recipients": recipients,
            "attachments": attachments
        }
        return f"Composed email: {email}"

class EmailCategorizationAgent:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = MultinomialNB()

    def train(self, emails, labels):
        X = self.vectorizer.fit_transform(emails)
        self.model.fit(X, labels)

    def run(self, emails):
        X = self.vectorizer.transform(emails)
        predictions = self.model.predict(X)
        return dict(zip(emails, predictions))

class EmailSummarizationAgent:
    def __init__(self):
        self.summarizer = pipeline('summarization')

    def run(self, email_body):
        summary = self.summarizer(email_body, max_length=50, min_length=25, do_sample=False)
        return summary[0]['summary_text']

class EmailAnalyticsAgent:
    def run(self, emails):
        df = pd.DataFrame(emails)
        fig = px.bar(df, x='sender', y='subject', title='Emails by Sender')
        fig.show()

class SecurityAndComplianceAgent:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, email_body):
        encrypted_text = self.cipher.encrypt(email_body.encode())
        return encrypted_text

    def decrypt(self, encrypted_body):
        decrypted_text = self.cipher.decrypt(encrypted_body).decode()
        return decrypted_text

    def run(self, email_body):
        encrypted_body = self.encrypt(email_body)
        decrypted_body = self.decrypt(encrypted_body)
        return {
            "encrypted_body": encrypted_body,
            "decrypted_body": decrypted_body
        }

# Command-Line Interface (CLI)
def cli():
    parser = argparse.ArgumentParser(description="Email Management Tool")
    parser.add_argument('--compose', action='store_true', help='Compose a new email')
    parser.add_argument('--categorize', action='store_true', help='Categorize emails')
    parser.add_argument('--summarize', action='store_true', help='Summarize an email')
    parser.add_argument('--analytics', action='store_true', help='Show email analytics')
    parser.add_argument('--secure', action='store_true', help='Encrypt and decrypt an email')

    args = parser.parse_args()

    if args.compose:
        subject = input("Enter the subject: ")
        body = input("Enter the body: ")
        recipients = input("Enter recipients (comma-separated): ").split(',')
        agent = EmailCompositionAgent()
        result = agent.run(subject, body, recipients)
        print(result)
    elif args.categorize:
        emails = [
            "Urgent: Meeting tomorrow",
            "Project update required",
            "Lunch plans for the weekend"
        ]
        agent = EmailCategorizationAgent()
        result = agent.run(emails)
        print(result)
    elif args.summarize:
        email_body = input("Enter the email body to summarize: ")
        agent = EmailSummarizationAgent()
        result = agent.run(email_body)
        print(result)
    elif args.analytics:
        emails = [
            {"subject": "Meeting tomorrow", "sender": "alice@example.com"},
            {"subject": "Project update", "sender": "bob@example.com"},
            {"subject": "Weekend plans", "sender": "charlie@example.com"}
        ]
        agent = EmailAnalyticsAgent()
        agent.run(emails)
    elif args.secure:
        email_body = input("Enter the email body to secure: ")
        agent = SecurityAndComplianceAgent()
        result = agent.run(email_body)
        print(result)
    else:
        print("Invalid choice")

# Web Interface using Flask
app = Flask(__name__)

@app.route('/compose', methods=['POST'])
def compose_email():
    data = request.json
    subject = data.get('subject')
    body = data.get('body')
    recipients = data.get('recipients')
    agent = EmailCompositionAgent()
    result = agent.run(subject, body, recipients)
    return jsonify(result)

@app.route('/categorize', methods=['POST'])
def categorize_emails():
    emails = request.json.get('emails')
    agent = EmailCategorizationAgent()
    result = agent.run(emails)
    return jsonify(result)

@app.route('/summarize', methods=['POST'])
def summarize_email():
    email_body = request.json.get('email_body')
    agent = EmailSummarizationAgent()
    result = agent.run(email_body)
    return jsonify(result)

@app.route('/analytics', methods=['POST'])
def email_analytics():
    emails = request.json.get('emails')
    agent = EmailAnalyticsAgent()
    agent.run(emails)
    return jsonify({"status": "Analytics displayed"})

@app.route('/secure', methods=['POST'])
def secure_email():
    email_body = request.json.get('email_body')
    agent = SecurityAndComplianceAgent()
    result = agent.run(email_body)
    return jsonify(result)

if __name__ == "__main__":
    mode = input("Enter mode ('cli' for command-line, 'web' for web server): ")
    if mode == 'cli':
        cli()
    elif mode == 'web':
        app.run(debug=True)
    else:
        print("Invalid mode. Use 'cli' or 'web'.")
