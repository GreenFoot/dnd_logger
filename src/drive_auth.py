"""Google Drive OAuth2 authentication helpers."""

import logging
import os

from PySide6.QtCore import QObject, QThread, Signal

from .utils import project_root

log = logging.getLogger(__name__)

_TOKEN_FILE = "drive_token.json"


def _token_path() -> str:
    return os.path.join(project_root(), _TOKEN_FILE)


def load_credentials():
    """Load saved credentials from disk, auto-refreshing if expired.

    Returns google.oauth2.credentials.Credentials or None.
    """
    path = _token_path()
    if not os.path.exists(path):
        return None
    try:
        from google.oauth2.credentials import Credentials

        creds = Credentials.from_authorized_user_file(path)
        if creds and creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request

            creds.refresh(Request())
            save_credentials(creds)
        return creds if creds and creds.valid else None
    except Exception:
        log.exception("Failed to load Drive credentials")
        return None


def save_credentials(creds) -> None:
    """Persist credentials (including refresh token) to disk."""
    path = _token_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    except Exception:
        log.exception("Failed to save Drive credentials")


def delete_credentials() -> None:
    """Remove saved credentials from disk."""
    path = _token_path()
    if os.path.exists(path):
        os.remove(path)


def get_user_email(creds) -> str:
    """Fetch the authenticated user's email address."""
    try:
        from googleapiclient.discovery import build

        service = build("oauth2", "v2", credentials=creds)
        info = service.userinfo().get().execute()  # pylint: disable=no-member
        return info.get("email", "")
    except Exception:
        return ""


class DriveAuthWorker(QObject):
    """Runs the OAuth2 installed-app flow in a background thread."""

    auth_completed = Signal(object)  # google.oauth2.credentials.Credentials
    auth_failed = Signal(str)

    def run(self):
        """Run the OAuth2 installed-app flow."""
        try:
            from google_auth_oauthlib.flow import InstalledAppFlow

            from .drive_credentials import CLIENT_CONFIG, SCOPES

            flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
            creds = flow.run_local_server(port=0)
            save_credentials(creds)
            self.auth_completed.emit(creds)
        except Exception as e:
            self.auth_failed.emit(str(e))


def start_auth_flow() -> tuple:
    """Create auth worker + thread. Returns (thread, worker)."""
    thread = QThread()
    worker = DriveAuthWorker()
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.auth_completed.connect(thread.quit)
    worker.auth_failed.connect(thread.quit)
    return thread, worker
