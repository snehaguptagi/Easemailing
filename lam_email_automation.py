import os
import openai
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Initialize OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_email_content(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating email content: {e}")
        return "Error generating email content."

def send_email(subject, body, to_email, from_email="your-email@example.com"):
    # Initialize the SendGrid client
    sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
    
    # Create the email message
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=body
    )
    
    try:
        # Send the email
        response = sg.send(message)
        print(f"Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

def automate_emailing(prompt, subject, to_email, from_email):
    # Generate email content
    email_body = generate_email_content([{"role": "system", "content": "You are a helpful assistant."},
                                          {"role": "user", "content": prompt}])
    
    # Send the email
    send_email(subject, email_body, to_email, from_email)

# Example usage
automate_emailing(
    prompt="Write a follow-up email after a job interview.",
    subject="Follow-Up After Interview",
    to_email="hiring.manager@example.com",
    from_email="your-email@example.com"
)
