"""Optional live Gmail provider.

Used only when AIEA_MODE=live and Gmail OAuth is configured. Everything is
imported lazily and guarded so that demo mode never needs the google libraries
installed. To enable:

  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
  # Download an OAuth client secret from Google Cloud Console (Desktop app) and:
  export GMAIL_CREDENTIALS=/path/to/credentials.json   # OAuth client secret
  export GMAIL_TOKEN=/path/to/token.json               # written after first auth

The first call opens a browser to authorize read + compose scopes.
"""
from __future__ import annotations

import base64
import os
from email.mime.text import MIMEText

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]


class GmailUnavailable(RuntimeError):
    """Raised when live Gmail is requested but not configured."""


def _service():
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError as exc:  # pragma: no cover
        raise GmailUnavailable(
            "Google API libraries not installed. Run: pip install "
            "google-api-python-client google-auth-httplib2 google-auth-oauthlib"
        ) from exc

    cred_path = os.getenv("GMAIL_CREDENTIALS")
    token_path = os.getenv("GMAIL_TOKEN", "token.json")
    if not cred_path or not os.path.exists(cred_path):
        raise GmailUnavailable("GMAIL_CREDENTIALS not set or file missing.")

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as fh:
            fh.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def is_available() -> bool:
    cred_path = os.getenv("GMAIL_CREDENTIALS")
    return bool(cred_path and os.path.exists(cred_path))


def _header(headers: list, name: str) -> str:
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def list_inbox(limit: int = 15) -> list[dict]:
    svc = _service()
    resp = svc.users().messages().list(userId="me", labelIds=["INBOX"], maxResults=limit).execute()
    out = []
    for ref in resp.get("messages", []):
        msg = svc.users().messages().get(userId="me", id=ref["id"], format="full").execute()
        payload = msg.get("payload", {})
        headers = payload.get("headers", [])
        out.append({
            "id": msg["id"],
            "from": _header(headers, "From"),
            "subject": _header(headers, "Subject") or "(no subject)",
            "received": _header(headers, "Date"),
            "unread": "UNREAD" in msg.get("labelIds", []),
            "body": msg.get("snippet", ""),
        })
    return out


def create_draft(to: str, subject: str, body: str) -> str:
    svc = _service()
    mime = MIMEText(body)
    mime["to"] = to
    mime["subject"] = subject
    raw = base64.urlsafe_b64encode(mime.as_bytes()).decode()
    draft = svc.users().drafts().create(userId="me", body={"message": {"raw": raw}}).execute()
    return draft.get("id", "")
