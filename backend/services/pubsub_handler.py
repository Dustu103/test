import base64
import json
from services.gmail_service import GmailService
from auth.gmail_auth import GmailOAuth

class PubSubHandler:
    def __init__(self, email):
        self.email = email
        self.credentials = GmailOAuth.get_credentials_for_email(email)
        self.gmail_service = GmailService(self.credentials)

    def handle_notification(self, envelope):
        message_data = envelope.get("message", {}).get("data")
        if not message_data:
            print("⚠️ No data in Pub/Sub message")
            return

        payload = json.loads(base64.b64decode(message_data).decode("utf-8"))
        history_id = payload.get("historyId")
        print(f"📨 New Gmail activity — History ID: {history_id}")

        message_ids = self.gmail_service.fetch_new_message_ids(history_id)
        for msg_id in message_ids:
            body = self.gmail_service.get_email_body(msg_id)
            print(f"📬 Email Body for {msg_id}:\n{body}")
