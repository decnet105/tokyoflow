#!/usr/bin/env python3
"""
TokyoFlow YouTube OAuth Authentication Engine
Acquires and refreshes OAuth2 credentials with YouTube upload and management scopes.
"""

import os
import sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

AUTH_DIR = Path(__file__).resolve().parent / "auth"
CLIENT_SECRETS_FILE = AUTH_DIR / "client_secrets.json"
TOKEN_FILE = AUTH_DIR / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtubepartner"
]

def get_authenticated_service():
    """Returns valid google credentials, triggering browser authorization if needed."""
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    
    if not CLIENT_SECRETS_FILE.exists():
        print(f" Error: Client secret file not found at {CLIENT_SECRETS_FILE}")
        sys.exit(1)

    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print(" Refreshing existing YouTube OAuth access token...")
            creds.refresh(Request())
        else:
            print(" Initiating new YouTube OAuth Flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRETS_FILE),
                SCOPES
            )
            # Try running local server
            try:
                creds = flow.run_local_server(port=8080, prompt="consent", access_type="offline")
            except Exception as e:
                print(f" Local server flow encountered: {e}. Falling back to console flow...")
                creds = flow.run_console()

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
            print(f" Token saved successfully to {TOKEN_FILE}")

    return creds

if __name__ == "__main__":
    print("==================================================")
    print(" TokyoFlow YouTube Authentication Setup")
    print("==================================================")
    creds = get_authenticated_service()
    print(" Authorization successful! Valid token is ready for automated uploads.")
