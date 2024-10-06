# Easemailing

## Purpose
Easemailing is a Python-based application that automates email content generation and sending using the OpenAI API and SendGrid. The goal is to streamline communication processes by making it easier to create and send professional emails.

## Features
- Generate email content using OpenAI's language model.
- Send emails using SendGrid.
- Extract details from incoming emails using regex.

## Setup Instructions

### Prerequisites
- Python 3.x
- An OpenAI API key
- A SendGrid API key
- Gmail API credentials (for accessing Gmail)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/easemailing.git
   cd easemailing

Install dependencies:
pip install -r requirements.txt

Create a .env file in the root directory and add your API keys:
OPENAI_API_KEY=your-openai-api-key
SENDGRID_API_KEY=your-sendgrid-api-key

Obtain Gmail API credentials and save them as credentials.json.

Usage
To generate and send an email, run:
python main.py
You can modify the email prompts and recipients in the code.

Contributing
Contributions are welcome! Please open an issue or submit a pull request.

License
This project is licensed under the MIT License.

#### Code Comments
Make sure each function has a clear docstring and inline comments as shown in the previous response for `email_extraction.py`. Apply this to all Python files.

---

### 2. Environment Configuration

#### `.env` File
Create a `.env` file in your project root to store sensitive information:

OPENAI_API_KEY=your-openai-api-key SENDGRID_API_KEY=your-sendgrid-api-key


#### `requirements.txt`
Ensure your `requirements.txt` includes all necessary dependencies:
```plaintext
openai
sendgrid
python-dotenv
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
praw
schedule




