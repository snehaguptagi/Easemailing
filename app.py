from flask import Flask, request, jsonify
from email_utils import generate_email_content, send_email

app = Flask(Easemailing)

@app.route('/generate-email', methods=['POST'])
def generate_email():
    data = request.json
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    content = generate_email_content(prompt)
    return jsonify({"content": content})

@app.route('/send-email', methods=['POST'])
def send_email_route():
    data = request.json
    to_email = data.get('to_email')
    subject = data.get('subject', 'No Subject')
    content = data.get('content', '')

    if not to_email or not content:
        return jsonify({"error": "Email and content are required"}), 400

    result = send_email(to_email, subject, content)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
