import openai

# Initialize OpenAI API
openai.api_key = 'your-openai-api-key'

def generate_email_content(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use "gpt-3.5-turbo" if you are using GPT-3.5
        messages=messages,
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

# Example messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Write a professional email to thank a client for their recent purchase and encourage them to leave a review."}
]
email_content = generate_email_content(messages)
print(email_content)
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(subject, body, to_email, from_email="your-email@example.com"):
    # Initialize the SendGrid client
    sg = SendGridAPIClient('your-sendgrid-api-key')
    
    # Create the email message
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=body)
    
    try:
        # Send the email
        response = sg.send(message)
        print(f"Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
send_email(
    subject="Thank You for Your Purchase!",
    body=email_content,
    to_email="client@example.com"
)
def automate_emailing(prompt, subject, to_email, from_email):
    # Generate email content
    email_body = generate_email_content(prompt)
    
    # Send the email
    send_email(subject, email_body, to_email, from_email)

# Example usage
automate_emailing(
    prompt="Write a follow-up email after a job interview.",
    subject="Follow-Up After Interview",
    to_email="hiring.manager@example.com",
    from_email="your-email@example.com"
)
