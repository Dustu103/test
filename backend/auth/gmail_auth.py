import os
import json
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from config import CLIENT_SECRET_FILE, REDIRECT_URI, SCOPES, TOKEN_DIR


class GmailOAuth:
    def __init__(self):
        self.credentials = None

    def get_auth_url(self):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE, scopes=SCOPES
        )
        flow.redirect_uri = REDIRECT_URI
        auth_url, _ = flow.authorization_url(access_type="offline", prompt="consent")
        return auth_url

    def exchange_code(self, code):
        flow = Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES)
        flow.redirect_uri = REDIRECT_URI
        flow.fetch_token(code=code)
        self.credentials = flow.credentials
        self._save_token(self.credentials)
        return self.credentials

    def _save_token(self, creds):
        from utils.token_storage import save_token
        user_email = self._get_user_email(creds)
        save_token(user_email, creds)

    def _get_user_email(self, creds):
        from googleapiclient.discovery import build
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        return profile['emailAddress']

    def load_credentials(self, email):
        from utils.token_storage import load_token
        self.credentials = load_token(email)
        return self.credentials
    
    def get_credentials_for_email(email):
        return GmailOAuth().load_credentials(email)

