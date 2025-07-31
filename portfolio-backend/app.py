from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not (name and email and message):
        return jsonify({"error": "Missing fields"}), 400

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        body = f"From: {name} <{email}>\n\n{message}"
        server.sendmail(os.getenv("EMAIL_USER"), os.getenv("EMAIL_USER"), body)
        server.quit()
        return jsonify({"message": "Message sent successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
