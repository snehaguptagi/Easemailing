from flask import Flask, request, jsonify
from email_utils import generate_email_content, send_email
import logging
import os

# Initialize Flask app
app = Flask("Easemailing")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "OK"}), 200

@app.route('/generate-email', methods=['POST'])
def generate_email():
    """Generate email content based on a prompt."""
    try:
        data = request.json
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            logging.warning("No prompt provided in request.")
            return jsonify({"error": "No prompt provided"}), 400

        content = generate_email_content(prompt)
        return jsonify({"content": content}), 200

    except Exception as e:
        logging.error(f"Error in /generate-email: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/send-email', methods=['POST'])
def send_email_route():
    """Send an email with the provided details."""
    try:
        data = request.json
        to_email = data.get('to_email', '').strip()
        subject = data.get('subject', 'No Subject').strip()
        content = data.get('content', '').strip()

        if not to_email or not content:
            logging.warning("Missing required fields: to_email or content.")
            return jsonify({"error": "Email and content are required"}), 400

        # Validate email format (basic check)
        if '@' not in to_email or '.' not in to_email:
            logging.warning("Invalid email format.")
            return jsonify({"error": "Invalid email format"}), 400

        result = send_email(to_email, subject, content)
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Error in /send-email: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Determine debug mode from environment variable
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
