import os

CLIENT_SECRET_FILE = "./client_secret.json"
REDIRECT_URI = "http://localhost:5000/callback"

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']
TOKEN_DIR = "backend/tokens"

os.makedirs(TOKEN_DIR, exist_ok=True)
