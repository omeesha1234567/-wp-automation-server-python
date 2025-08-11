from flask import Flask, request
from twilio.rest import Client
import requests
import os

app = Flask(__name__)

# Twilio credentials from environment variables
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+17756407218"  # Twilio sandbox number

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Flowise API endpoint (must be PUBLIC, not localhost)
FLOWISE_API_URL = os.environ.get("FLOWISE_API_URL")

# Test route for Render
@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Automation Server is Running 🚀"

# WhatsApp webhook route
@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')

    # Send message to Flowise
    payload = {"question": incoming_msg}
    try:
        flowise_response = requests.post(FLOWISE_API_URL, json=payload)
        if flowise_response.status_code == 200:
            reply = flowise_response.json().get("text", "Sorry, I couldn't get a reply.")
        else:
            reply = "Error contacting Flowise."
    except Exception as e:
        reply = f"Error: {str(e)}"

    # Send reply via Twilio WhatsApp
    try:
        client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=reply,
            to=from_number
        )
    except Exception as e:
        return f"Failed to send message via Twilio: {str(e)}", 500

    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)

