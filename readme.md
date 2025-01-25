# Easemailing

[![Website Status](https://img.shields.io/website?url=https%3A%2F%2Feasemailing.in)](https://easemailing6.wordpress.com/)  
[![First Timers](https://img.shields.io/badge/first--timers--friendly-blue.svg?style=flat-square)](https://www.firsttimersonly.com/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Easemailing is a Python-based application that automates email content generation and sending using OpenAI and SendGrid. It simplifies communication by generating professional emails effortlessly.

## Features
- **AI-Powered Content**: Generate email content using OpenAI's API.
- **Email Automation**: Send emails with Gmail SMTP.
- **Email Parsing**: Extract details from incoming emails using regex.

## Prerequisites
- Python 3.x
- OpenAI API Key (or free Hugging Face models)
- Gmail API credentials (as `credentials.json`)

## Installation

### Clone the Repository
```bash
git clone https://github.com/sneha-81/easemailing.git
cd easemailing
Install Dependencies
Use pip to install required packages:

bash
Copy
Edit
pip install -r requirements.txt
Setup Gmail API
Visit the Google Cloud Console.
Create a new project and enable the Gmail API.
Download your credentials.json file and place it in the project root.
Environment Variables
Create a .env file with the following keys:

env
Copy
Edit
OPENAI_API_KEY=your_openai_api_key
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password  # Gmail App Password or OAuth token
Usage
Modify email prompts and recipient details in the script if needed.
Run the application:
bash
Copy
Edit
python app.py
Contribution Guide
We welcome contributions from everyone! Here's how you can help:

Fork the repository.
Clone your fork:
bash
Copy
Edit
git clone https://github.com/your-username/easemailing.git
Create a feature branch:
bash
Copy
Edit
git checkout -b feature-name
Commit your changes and push:
bash
Copy
Edit
git add .
git commit -m "Description of your feature"
git push origin feature-name
Submit a pull request.
License
This project is licensed under the MIT License.

Acknowledgements
OpenAI for their language model.
Gmail for seamless email interactions.
vbnet
Copy
Edit

You can replace the current `README.md` file content with the above text. Let me know if you need further help!
