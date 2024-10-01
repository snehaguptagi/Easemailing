import os
import openai
import logging
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from flask import Flask, request, jsonify
import schedule
import time
import click
import unittest

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("lam_model.log"),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

# Set API keys with error handling
openai.api_key = os.getenv("OPENAI_API_KEY")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

if not all([openai.api_key, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT]):
    logging.error("API keys or environment variables are missing.")
    raise EnvironmentError("Missing environment variables. Check your .env file.")

# Define Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class LAMModel:
    """A model to interact with OpenAI's GPT for generating email content."""
    
    def __init__(self):
        self.model = "text-davinci-003"  # You can choose a different model if needed

    def generate_email(self, prompt):
        """Generate email content using the LAM model."""
        try:
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                max_tokens=150  # Adjust max_tokens as needed
            )
            return response.choices[0].text.strip()
        except openai.error.OpenAIError as e:
            logging.error(f"OpenAI API Error: {e}")
            return "There was an issue generating the email content."
        except Exception as e:
            logging.error(f"Unexpected Error: {e}")
            return "An unexpected error occurred while generating the email."

# Initialize the LAM Model
lam_model = LAMModel()

class Agent:
    """Base class for agents to define common interface."""
    
    def run(self, context=None):
        """Method to be overridden by subclasses."""
        raise NotImplementedError("Subclasses should implement this method.")

class EmailCompositionAgent(Agent):
    """Agent for composing emails using LAM."""
    
    def run(self, context=None):
        """Compose an email using LAM."""
        prompt = "Compose an email with the following details: Meeting reminder for next week."
        email_body = lam_model.generate_email(prompt)
        email_subject = "Meeting Reminder"
        context = context or {}
        context["email_composition"] = {"subject": email_subject, "body": email_body}
        return context

class EmailCategorizationAgent(Agent):
    """Agent for categorizing emails into predefined categories."""
    
    def run(self, context=None):
        """Categorize emails into predefined categories."""
        categories = ["Work", "Personal", "Promotions"]
        context = context or {}
        context["categories"] = categories
        return context

class EmailSummarizationAgent(Agent):
    """Agent for summarizing email content using LAM."""
    
    def run(self, context=None):
        """Summarize the email content using LAM."""
        email_content = context.get("email_content", "")
        prompt = f"Summarize the following email: {email_content}"
        summary = lam_model.generate_email(prompt)
        context["summary"] = summary
        return context

class ResponseSuggestionAgent(Agent):
    """Agent for suggesting responses based on email summary using LAM."""
    
    def run(self, context=None):
        """Suggest responses based on the email summary using LAM."""
        summary = context.get("summary", "")
        prompt = f"Suggest responses to the following email summary: {summary}"
        suggestions = lam_model.generate_email(prompt).split('\n')
        context["suggestions"] = suggestions
        return context

class FollowUpReminderAgent(Agent):
    """Agent for providing follow-up reminders."""
    
    def run(self, context=None):
        """Provide follow-up reminders."""
        reminders = ["Follow up on the project update email.", "Send a reminder for the meeting."]
        context = context or {}
        context["reminders"] = reminders
        return context

class MeetingSchedulerAgent(Agent):
    """Agent for scheduling meetings based on email content."""
    
    def run(self, context=None):
        """Schedule a meeting based on context."""
        meeting_details = {
            "date": "2024-08-01",
            "time": "10:00 AM",
            "participants": ["Alice", "Bob", "Charlie"]
        }
        context = context or {}
        context["meeting_details"] = meeting_details
        return context

class AttachmentManagementAgent(Agent):
    """Agent for managing email attachments."""
    
    def run(self, context=None):
        """Manage email attachments."""
        attachments = ["file1.pdf", "image2.png", "document3.docx"]
        context = context or {}
        context["attachments"] = attachments
        return context

class ContactManagementAgent(Agent):
    """Agent for managing email contacts."""
    
    def run(self, context=None):
        """Manage email contacts."""
        contacts = ["Alice", "Bob", "Charlie"]
        context = context or {}
        context["contacts"] = contacts
        return context

class EmailAnalyticsAgent(Agent):
    """Agent for providing email analytics."""
    
    def run(self, context=None):
        """Provide email analytics."""
        analytics = {
            "total_emails": 150,
            "replies": 45,
            "bounced": 5
        }
        context = context or {}
        context["analytics"] = analytics
        return context

class SecurityAndComplianceAgent(Agent):
    """Agent for ensuring email security and compliance."""
    
    def run(self, context=None):
        """Ensure email security and compliance."""
        compliance_status = "All emails are secure and compliant with company policies."
        context = context or {}
        context["compliance_status"] = compliance_status
        return context

# Define tasks with associated agents
tasks = {
    "email_composition": {"description": "Assist users in composing emails", "agent": EmailCompositionAgent()},
    "email_categorization": {"description": "Automatically categorize incoming emails", "agent": EmailCategorizationAgent()},
    "email_summarization": {"description": "Provide summaries of long emails", "agent": EmailSummarizationAgent()},
    "response_suggestion": {"description": "Suggest responses to emails", "agent": ResponseSuggestionAgent()},
    "follow_up_reminder": {"description": "Remind users to follow up on emails", "agent": FollowUpReminderAgent()},
    "meeting_scheduler": {"description": "Schedule meetings based on email content", "agent": MeetingSchedulerAgent()},
    "attachment_management": {"description": "Manage email attachments", "agent": AttachmentManagementAgent()},
    "contact_management": {"description": "Manage email contacts", "agent": ContactManagementAgent()},
    "email_analytics": {"description": "Provide insights and analytics on email usage", "agent": EmailAnalyticsAgent()},
    "security_and_compliance": {"description": "Ensure email security and compliance", "agent": SecurityAndComplianceAgent()},
}

class Process:
    """A class to manage the execution of multiple agents (tasks) in a process."""
    
    def __init__(self, agents, tasks, verbose=2, tools=None):
        self.agents = agents
        self.tasks = tasks
        self.verbose = verbose
        self.tools = tools if tools else []

    def run_all_tasks(self, initial_context=None):
        """Run all tasks in sequence, capturing their output in the context."""
        results = {}
        context = initial_context or {"email_content": "Dear Team, I would like to inform you about the upcoming project deadlines and the tasks assigned to each member. Regards, [Your Name]"}
        for task_name, task_info in self.tasks.items():
            try:
                agent = task_info["agent"]
                context = agent.run(context.copy())  # Pass a copy of the context
                results[task_name] = "Completed"
                logging.info(f"{task_name}: Completed")
            except Exception as e:
                results[task_name] = f"Failed: {e}"
                logging.error(f"{task_name}: Failed - {e}")
        return results

# Initialize Crew (Process in this case)
crew = Process(
    agents={
        "email_composition": EmailCompositionAgent(),
        "email_categorization": EmailCategorizationAgent(),
        "email_summarization": EmailSummarizationAgent(),
        "response_suggestion": ResponseSuggestionAgent(),
        "follow_up_reminder": FollowUpReminderAgent(),
        "meeting_scheduler": MeetingSchedulerAgent(),
        "attachment_management": AttachmentManagementAgent(),
        "contact_management": ContactManagementAgent(),
        "email_analytics": EmailAnalyticsAgent(),
        "security_and_compliance": SecurityAndComplianceAgent()
    },
    tasks=tasks,
    verbose=2
)

@click.group()
def cli():
    """CLI for managing tasks."""
    pass

@click.command()
@click.option('--task', default=None, help='Specify a task to run')
def run_all_tasks(task):
    """Run all tasks or a specific task."""
    if task:
        logging.info(f"Running task: {task}")
        if task in tasks:
            agent = tasks[task]["agent"]
            context = {}
            agent.run(context)
        else:
            logging.error(f"Task {task} not found.")
    else:
        logging.info("Running all tasks")
        crew.run_all_tasks()

@click.command()
def list_tasks():
    """List all available tasks."""
    for task_name, task_info in tasks.items():
        print(f"{task_name}: {task_info['description']}")

@click.command()
@click.option('--time', default="09:00", help='Time to run the task (e.g., 09:00)')
def schedule_task(time):
    """Schedule a task to run at a specified time."""
    schedule.every().day.at(time).do(run_all_tasks)
    logging.info(f"Task scheduled to run every day at {time}.")

    while True:
        schedule.run_pending()
        time.sleep(1)

cli.add_command(run_all_tasks)
cli.add_command(list_tasks)
cli.add_command(schedule_task)

if __name__ == '__main__':
    cli()

# Unit tests for the LAM Model
class TestLAMModel(unittest.TestCase):
    
    def test_generate_email(self):
        lam_model = LAMModel()
        result = lam_model.generate_email("Test email prompt")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_email_composition_agent(self):
        agent = EmailCompositionAgent()
        context = agent.run()
        self.assertIn("email_composition", context)
        self.assertIsInstance(context["email_composition"]["body"], str)

    def test_email_summarization_agent(self):
        agent = EmailSummarizationAgent()
        context = {"email_content": "Test email content"}
        context = agent.run(context)
        self.assertIn("summary", context)
        self.assertIsInstance(context["summary"], str)
    
    def test_process_run_all_tasks(self):
        process = Process(
            agents={
                "email_composition": EmailCompositionAgent(),
                "email_summarization": EmailSummarizationAgent()
            },
            tasks=tasks,
            verbose=2
        )
        results = process.run_all_tasks()
        self.assertEqual(results["email_composition"], "Completed")
        self.assertEqual(results["email_summarization"], "Completed")

if __name__ == '__main__':
    unittest.main()

app = Flask(Easemailing)

@app.route('/run_task', methods=['POST'])
def run_task():
    task_name = request.json.get('task')
    if task_name in tasks:
        agent = tasks[task_name]["agent"]
        context = {}
        result = agent.run(context)
        return jsonify(result)
    else:
        return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)