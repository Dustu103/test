import os
import json
from google.oauth2.credentials import Credentials
from config import TOKEN_DIR

def save_token(email, creds):
    token_data = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes,
    }
    with open(os.path.join(TOKEN_DIR, f"token_{email}.json"), "w") as f:
        json.dump(token_data, f)

def load_token(email):
    with open(os.path.join(TOKEN_DIR, f"token_{email}.json"), "r") as f:
        token_data = json.load(f)
        return Credentials.from_authorized_user_info(token_data)
