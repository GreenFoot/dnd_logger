"""Auto-update from GitHub Releases."""

import json
import logging
import os
import tempfile
import urllib.request
import urllib.error

from PySide6.QtCore import QObject, QThread, Signal

from . import __version__

log = logging.getLogger(__name__)

_API_URL = "https://api.github.com/repos/GreenFoot/dnd_logger/releases/latest"


def parse_version(s: str) -> tuple[int, ...]:
    """Parse a version string like 'v1.2.3' or '0.0.0-dev' into a comparable tuple."""
    s = s.strip().lstrip("v")
    s = s.split("-")[0]  # strip -dev, -rc1, etc.
    parts = []
    for p in s.split("."):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    return tuple(parts)


# ── Check worker ─────────────────────────────────────────


class UpdateCheckWorker(QObject):
    """Check GitHub for a newer release."""

    update_available = Signal(str, str, str, str)  # tag, name, download_url, body
    no_update = Signal()
    error = Signal(str)

    def run(self):
        try:
            req = urllib.request.Request(
                _API_URL,
                headers={"Accept": "application/vnd.github.v3+json",
                         "User-Agent": "DnDLogger-Updater"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())

            tag = data.get("tag_name", "")
            name = data.get("name", tag)
            body = data.get("body", "")

            remote = parse_version(tag)
            local = parse_version(__version__)

            if remote <= local:
                self.no_update.emit()
                return

            # Find the .exe installer asset
            download_url = ""
            for asset in data.get("assets", []):
                if asset.get("name", "").lower().endswith(".exe"):
                    download_url = asset["browser_download_url"]
                    break

            if not download_url:
                self.error.emit("Aucun installateur trouvé dans cette release.")
                return

            self.update_available.emit(tag, name, download_url, body)

        except urllib.error.URLError as e:
            self.error.emit(f"Erreur réseau : {e.reason}")
        except Exception as e:
            self.error.emit(str(e))


# ── Download worker ──────────────────────────────────────


class UpdateDownloadWorker(QObject):
    """Download an installer asset in chunks."""

    progress = Signal(int, int)  # downloaded, total
    completed = Signal(str)      # local file path
    error = Signal(str)

    def __init__(self, url: str):
        super().__init__()
        self._url = url
        self._cancelled = False
        self._tmp_path = ""

    def cancel(self):
        self._cancelled = True

    def run(self):
        try:
            req = urllib.request.Request(
                self._url,
                headers={"User-Agent": "DnDLogger-Updater"},
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                total = int(resp.headers.get("Content-Length", 0))
                tmp = tempfile.NamedTemporaryFile(
                    suffix=".exe", delete=False, dir=tempfile.gettempdir()
                )
                self._tmp_path = tmp.name

                downloaded = 0
                while True:
                    if self._cancelled:
                        tmp.close()
                        self._cleanup_tmp()
                        return
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    tmp.write(chunk)
                    downloaded += len(chunk)
                    self.progress.emit(downloaded, total)
                tmp.close()

            self.completed.emit(self._tmp_path)

        except Exception as e:
            self._cleanup_tmp()
            self.error.emit(str(e))

    def _cleanup_tmp(self):
        if self._tmp_path and os.path.exists(self._tmp_path):
            try:
                os.unlink(self._tmp_path)
            except OSError:
                pass


# ── Factory helpers ──────────────────────────────────────


def start_update_check() -> tuple[QThread, UpdateCheckWorker]:
    """Create and wire a QThread + UpdateCheckWorker pair (caller must start)."""
    thread = QThread()
    worker = UpdateCheckWorker()
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    return thread, worker


def start_update_download(url: str) -> tuple[QThread, UpdateDownloadWorker]:
    """Create and wire a QThread + UpdateDownloadWorker pair (caller must start)."""
    thread = QThread()
    worker = UpdateDownloadWorker(url)
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    return thread, worker
