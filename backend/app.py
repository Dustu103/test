from flask import Flask, redirect, request, session, jsonify
from auth.gmail_auth import GmailOAuth
import os
import json
# from auth.gmail_auth import GmailOAuth.get_credentials_for_email
from services.gmail_service import GmailService
from services.pubsub_handler import PubSubHandler
import base64

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET')  # Set a secret key for session management
gmail_auth = GmailOAuth()

@app.route("/")
def home():
    print("✅ / route hit")
    return "✅ Backend working"

@app.route("/login")
def login():
    print("🔑 Redirecting to Google OAuth")
    return redirect(gmail_auth.get_auth_url())

@app.route("/callback")
def callback():
    print("🔁 OAuth callback received")
    code = request.args.get("code")
    creds = gmail_auth.exchange_code(code)
    session["email"] = gmail_auth._get_user_email(creds)
    gmail_service = GmailService(creds)

    topic_name = os.getenv("TOPIC_NAME")
    gmail_service.start_watch(topic_name)
    return jsonify({"message": "Authentication successful", "email": session["email"]})

# @app.before_request
# def register_gmail_watch():
#     email = session.get("email")
#     if not email:
#         print("⚠️ No email session found, skipping Gmail watch setup.")
#         return

#     creds = GmailOAuth.get_credentials_for_email(email)
#     gmail_service = GmailService(creds)

#     topic_name = f"projects/{os.getenv('PROJECT_ID')}/topics/gmail-mail-events"
#     gmail_service.start_watch(topic_name)

@app.route("/check-auth")
def check_auth():
    print("🔍 Checking auth")
    email = session.get("email")
    if not email:
        return jsonify({"auth": False})
    creds = gmail_auth.load_credentials(email)
    return jsonify({"auth": creds and creds.valid})



@app.route("/notifications", methods=["POST"])
def notifications():
    print("📩 Notification received")
    # envelope = request.get_json(force=True, silent=True)
    raw_body = json.loads(request.data.decode())
    print("Raw body:", raw_body)
    # if not envelope or "message" not in envelope:
    #     return "Invalid message format", 400

    # Decode base64 message data
    msg_data = raw_body["message"]
    
    # print("Decoded message data:", msg)
    # print("Message data:", msg_data["data"])
    # msg_data = envelope["message"].get("data")
    if not msg_data:
        return "Missing data", 400

    try:
        msg = base64.b64decode(msg_data["data"]).decode("utf-8")
        print("Decoded message:", msg)
        # return "OK", 200
        history_data = raw_body
        user_email = history_data.get("emailAddress")
        
        print("📧 Email from notification:", user_email)

        if user_email:
            handler = PubSubHandler(user_email)
            handler.handle_notification(history_data)
    except Exception as e:
        print("❌ Error handling notification:", e)
        return "Error", 400

    return "OK", 200


if __name__ == "__main__":
    print("🚀 Starting Flask backend on http://localhost:5000")
    app.run(port=5000, debug=True)
