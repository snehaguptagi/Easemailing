import re
from dateutil.parser import parse
from collections import namedtuple

EmailDetails = namedtuple('EmailDetails', ['dates', 'times', 'contacts', 'attachments'])

def extract_email_details(email_body: str) -> EmailDetails:
    details = {'dates': [], 'times': [], 'contacts': [], 'attachments': []}

    # Extract dates
    date_pattern = r'\b(\d{1,2} [A-Za-z]{3,9} \d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4})\b'
    dates = re.findall(date_pattern, email_body)
    if dates:
        details['dates'] = [parse(date).date() for date in dates]

    # Extract times
    time_pattern = r'\b\d{1,2}:\d{2} (?:AM|PM|am|pm)\b'
    times = re.findall(time_pattern, email_body)
    if times:
        details['times'] = times

    # Extract contact names
    contact_pattern = r'\b[A-Z][a-z]+(?: [A-Z][a-z]+)*\b'
    contacts = re.findall(contact_pattern, email_body)
    if contacts:
        details['contacts'] = contacts
    # Extract attachments (assuming attachments are mentioned in the email body)
    attachment_pattern = r'\b\w+\.\w{2,4}\b'
    attachments = re.findall(attachment_pattern, email_body)
    if attachments:
        details['attachments'] = attachments

    return EmailDetails(**details)

# Example usage
email_body = """
Hi Team,

Please find the project update attached. We have a meeting scheduled on 2024-08-01 at 10:00 AM.
Best Regards,
Alice Johnson
"""
extracted_details = extract_email_details(email_body)
print(extracted_details)
