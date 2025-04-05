from googleapiclient.discovery import build

class GmailService:
    def __init__(self, credentials):
        self.service = build('gmail', 'v1', credentials=credentials)

    def start_watch(self, topic_name):
        request = {
            'labelIds': ['INBOX'],
            'topicName': "projects/emailai-455810/topics/gmail-mail-events"
        }
        response = self.service.users().watch(userId='me', body=request).execute()
        print("🔔 Gmail Watch Registered:", response)
        return response.get('historyId')
    
    def fetch_new_message_ids(self, history_id):
        result = self.service.users().history().list(
            userId='me',
            startHistoryId=history_id,
            historyTypes=['messageAdded']
        ).execute()

        message_ids = []
        for record in result.get('history', []):
            for msg in record.get('messages', []):
                message_ids.append(msg['id'])

        return message_ids
    
    def get_email_body(self, message_id):
        message = self.service.users().messages().get(
            userId='me', id=message_id, format='full'
        ).execute()

        payload = message.get('payload', {})
        parts = payload.get('parts', [])
        body = ""

        for part in parts:
            if part.get('mimeType') == 'text/plain':
                data = part.get('body', {}).get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8")
                    break

        return body

    def get_service(self):
        return self.service
