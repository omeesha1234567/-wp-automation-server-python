from flask import Flask, request
from twilio.rest import Client
import requests
import os

app = Flask(__name__)

# Twilio credentials
ACCOUNT_SID = "your_account_sid"
AUTH_TOKEN = "your_auth_token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio sandbox number

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Flowise API endpoint (replace with your actual endpoint)
FLOWISE_API_URL = "http://localhost:3000/api/v1/prediction/your_agent_id"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')

    # Send message to Flowise
    payload = {"question": incoming_msg}
    flowise_response = requests.post(FLOWISE_API_URL, json=payload)
    
    if flowise_response.status_code == 200:
        reply = flowise_response.json().get("text", "Sorry, I couldn't get a reply.")
    else:
        reply = "Error contacting Flowise."

    # Send reply via Twilio WhatsApp
    client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=reply,
        to=from_number
    )

    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
