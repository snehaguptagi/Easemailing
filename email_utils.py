import openai
import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
from_email = os.getenv("FROM_EMAIL", "your_email@example.com")  # Default fallback

def generate_email_content(prompt, max_tokens=100, engine="text-davinci-003"):
    """Generate email content using OpenAI API."""
    try:
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=max_tokens
        )
        logging.info("Email content generated successfully.")
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Error generating email content: {str(e)}")
        raise RuntimeError("Failed to generate email content.") from e

def send_email(to_email, subject, content):
    """Send an email using SendGrid API."""
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        sg.send(message)
        logging.info(f"Email sent successfully to {to_email}.")
        return {"status": "success", "message": "Email sent successfully"}
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        return {"status": "error", "message": "Failed to send email."}
