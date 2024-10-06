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

Gmail API Credentials: Obtain credentials from the Google Developer Console and save them as credentials.json in the root directory.

Usage:
To generate and send an email, run:
python main.py
You can modify the email prompts and recipients in the code.

Contributing:
Contributions are welcome! If you find any bugs or have feature suggestions, please open an issue or submit a pull request.

License:
This project is licensed under the MIT License.

### 2. Code Comments

Make sure your Python code is well-commented for clarity. Here’s a guideline on how to add comments effectively:

#### General Guidelines for Code Comments

1. **Function Docstrings**: Each function should start with a docstring that describes:
   - What the function does.
   - Parameters it accepts (with types).
   - What it returns (with types).

2. **Inline Comments**: Use inline comments to explain complex logic or calculations within your functions.

#### Example: Commenting Code in `email_extraction.py`

Here's how you might add comments to your existing functions:

```python
import re
from dateutil.parser import parse

def extract_email_details(email_body):
    """
    Extracts details such as dates, times, contacts, and attachments from the given email body.
    
    Parameters:
        email_body (str): The text of the email to extract details from.
        
    Returns:
        dict: A dictionary containing lists of extracted dates, times, contacts, and attachments.
    """
    details = {}

    # Regex pattern to find dates in formats like "1 January 2024" or "2024-01-01"
    date_pattern = r'\b(\d{1,2} [A-Za-z]+ \d{4}|\d{4}-\d{2}-\d{2})\b'
    dates = re.findall(date_pattern, email_body)  # Find all date matches in the email body
    if dates:
        details['dates'] = [parse(date).date() for date in dates]  # Parse and store found dates

    # Regex pattern to find times in formats like "10:00 AM"
    time_pattern = r'\b\d{1,2}:\d{2} (?:AM|PM|am|pm)\b'
    times = re.findall(time_pattern, email_body)  # Find all time matches in the email body
    if times:
        details['times'] = times  # Store found times

    # Regex pattern to find contact names in "First Last" format
    contact_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
    contacts = re.findall(contact_pattern, email_body)  # Find all contact names
    if contacts:
        details['contacts'] = contacts  # Store found contacts

    # Regex pattern to find file attachments mentioned in the email body
    attachment_pattern = r'\b\w+\.\w+\b'
    attachments = re.findall(attachment_pattern, email_body)  # Find all attachment names
    if attachments:
        details['attachments'] = attachments  # Store found attachments

    return details  # Return the collected details as a dictionary











