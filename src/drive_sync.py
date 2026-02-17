"""Google Drive sync engine for shared campaign files."""

import enum
import hashlib
import json
import logging
import os
import threading
import time

from PySide6.QtCore import QMutex, QMutexLocker, QObject, QThread, QTimer, Signal

from .utils import (
    active_campaign_dir,
    active_campaign_name,
    campaign_drive_config,
    journal_path,
    project_root,
    quest_log_path,
    shared_config_path,
)

log = logging.getLogger(__name__)

_SYNC_STATE_FILE = "drive_sync_state.json"
_POLL_INTERVAL_MS = 30_000  # 30 seconds
_UPLOAD_DEBOUNCE_MS = 10_000  # 10 seconds
_APP_FOLDER_NAME = "DnD Logger"

# Files to sync: local filename → Drive remote name
SYNCABLE_FILES = {
    "quest_log.html": "quest_log.html",
    "journal.html": "journal.html",
    "shared_config.json": "shared_config.json",
}


class SyncStatus(enum.Enum):
    DISABLED = "disabled"
    IDLE = "idle"
    SYNCING = "syncing"
    CONFLICT = "conflict"
    ERROR = "error"
    OFFLINE = "offline"


class SyncDirection(enum.Enum):
    NONE = "none"
    UP = "up"        # local changed → upload
    DOWN = "down"    # remote changed → download
    CONFLICT = "conflict"  # both changed


# ---------------------------------------------------------------------------
# Drive API helpers (run in worker threads, never on the UI thread)
# ---------------------------------------------------------------------------

class DriveFolderManager:
    """Find or create campaign folders on Google Drive."""

    def __init__(self, service):
        self._service = service

    def get_or_create_campaign_folder(self, campaign_name: str) -> str:
        """Return the campaign folder ID, creating it if needed.

        Structure: My Drive / DnD Logger / <campaign_name> /
        """
        app_folder_id = self._find_or_create_folder(_APP_FOLDER_NAME, parent_id="root")
        campaign_folder_id = self._find_or_create_folder(campaign_name, parent_id=app_folder_id)
        return campaign_folder_id

    def _find_or_create_folder(self, name: str, parent_id: str) -> str:
        query = (
            f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder' "
            f"and '{parent_id}' in parents and trashed = false"
        )
        results = self._service.files().list(
            q=query, spaces="drive", fields="files(id, name)", pageSize=1
        ).execute()
        files = results.get("files", [])
        if files:
            return files[0]["id"]
        # Create
        metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id],
        }
        folder = self._service.files().create(body=metadata, fields="id").execute()
        return folder["id"]


class DriveFileManager:
    """Upload/download individual files in the campaign folder.

    All public methods are guarded by a threading lock because
    googleapiclient (httplib2) is NOT thread-safe.  Multiple worker
    threads share this instance, so every API call must be serialised.
    """

    def __init__(self, service, folder_id: str):
        self._service = service
        self._folder_id = folder_id
        self._file_id_cache: dict[str, str] = {}
        self._lock = threading.Lock()

    def upload_file(self, local_path: str, remote_name: str) -> dict:
        """Create or update a file in the campaign folder. Returns file metadata."""
        from googleapiclient.http import MediaFileUpload

        with self._lock:
            media = MediaFileUpload(local_path, resumable=True)
            file_id = self._find_file_unlocked(remote_name)

            if file_id:
                result = self._service.files().update(
                    fileId=file_id,
                    media_body=media,
                    fields="id, modifiedTime, md5Checksum",
                ).execute()
            else:
                metadata = {"name": remote_name, "parents": [self._folder_id]}
                result = self._service.files().create(
                    body=metadata,
                    media_body=media,
                    fields="id, modifiedTime, md5Checksum",
                ).execute()
                self._file_id_cache[remote_name] = result["id"]
            return result

    def download_file(self, remote_name: str, local_path: str) -> bool:
        """Download a file from Drive to local path. Returns True on success."""
        with self._lock:
            file_id = self._find_file_unlocked(remote_name)
            if not file_id:
                return False
            request = self._service.files().get_media(fileId=file_id)
            content = request.execute()
        with open(local_path, "wb") as f:
            f.write(content)
        return True

    def get_remote_metadata(self, remote_name: str) -> dict | None:
        """Get modifiedTime and md5Checksum without downloading."""
        with self._lock:
            file_id = self._find_file_unlocked(remote_name)
            if not file_id:
                return None
            return self._service.files().get(
                fileId=file_id,
                fields="id, modifiedTime, md5Checksum",
            ).execute()

    def _find_file_unlocked(self, name: str) -> str | None:
        """Look up a file ID — caller must hold self._lock."""
        if name in self._file_id_cache:
            return self._file_id_cache[name]
        query = (
            f"name = '{name}' and '{self._folder_id}' in parents "
            f"and trashed = false"
        )
        results = self._service.files().list(
            q=query, spaces="drive", fields="files(id)", pageSize=1
        ).execute()
        files = results.get("files", [])
        if files:
            self._file_id_cache[name] = files[0]["id"]
            return files[0]["id"]
        return None


# ---------------------------------------------------------------------------
# Sync state persistence
# ---------------------------------------------------------------------------

def _sync_state_path(cfg: dict) -> str:
    return os.path.join(active_campaign_dir(cfg), _SYNC_STATE_FILE)


def _load_sync_state(cfg: dict) -> dict:
    path = _sync_state_path(cfg)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_sync_state(state: dict, cfg: dict) -> None:
    path = _sync_state_path(cfg)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def _local_md5(filepath: str) -> str:
    """Compute MD5 of a local file."""
    h = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
    except OSError:
        return ""
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Worker objects for threaded Drive operations
# ---------------------------------------------------------------------------

class _UploadWorker(QObject):
    finished = Signal(str, dict)   # filename, metadata
    error = Signal(str, str)       # filename, error message

    def __init__(self, file_mgr: DriveFileManager, local_path: str, remote_name: str):
        super().__init__()
        self._file_mgr = file_mgr
        self._local_path = local_path
        self._remote_name = remote_name

    def run(self):
        try:
            meta = self._file_mgr.upload_file(self._local_path, self._remote_name)
            self.finished.emit(self._remote_name, meta)
        except Exception as e:
            self.error.emit(self._remote_name, str(e))


class _PollWorker(QObject):
    """Check remote metadata for all synced files."""
    finished = Signal(dict)  # {remote_name: metadata_or_None}
    error = Signal(str)

    def __init__(self, file_mgr: DriveFileManager, filenames: list[str]):
        super().__init__()
        self._file_mgr = file_mgr
        self._filenames = filenames

    def run(self):
        try:
            results = {}
            for name in self._filenames:
                log.debug("Checking remote metadata for: %s", name)
                results[name] = self._file_mgr.get_remote_metadata(name)
                log.debug("  -> %s", "found" if results[name] else "not found")
            self.finished.emit(results)
        except Exception as e:
            log.exception("Poll worker error: %s", e)
            self.error.emit(str(e))


class _DownloadWorker(QObject):
    finished = Signal(str)   # remote_name
    error = Signal(str, str)

    def __init__(self, file_mgr: DriveFileManager, remote_name: str, local_path: str):
        super().__init__()
        self._file_mgr = file_mgr
        self._remote_name = remote_name
        self._local_path = local_path

    def run(self):
        try:
            self._file_mgr.download_file(self._remote_name, self._local_path)
            self.finished.emit(self._remote_name)
        except Exception as e:
            self.error.emit(self._remote_name, str(e))


# ---------------------------------------------------------------------------
# Main sync engine
# ---------------------------------------------------------------------------

class DriveSyncEngine(QObject):
    """Orchestrates Google Drive sync for shared campaign files."""

    status_changed = Signal(SyncStatus)
    sync_completed = Signal()
    conflict_detected = Signal(str, str, str)  # filename, local_html, remote_html
    error_occurred = Signal(str)
    remote_file_updated = Signal(str)  # filename that was downloaded

    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self._config = config
        self._service = None
        self._folder_mgr: DriveFolderManager | None = None
        self._file_mgr: DriveFileManager | None = None
        self._sync_state = _load_sync_state(config)
        self._status = SyncStatus.DISABLED
        self._poll_timer = QTimer(self)
        self._poll_timer.timeout.connect(self._poll_remote)
        self._upload_timers: dict[str, QTimer] = {}
        self._active_threads: list[tuple[QThread, QObject]] = []  # (thread, worker) prevent GC
        self._mutex = QMutex()

    @property
    def status(self) -> SyncStatus:
        return self._status

    def _set_status(self, s: SyncStatus):
        if s != self._status:
            self._status = s
            self.status_changed.emit(s)

    def _local_path_for(self, remote_name: str) -> str:
        """Map a remote filename to its local path."""
        if remote_name == "quest_log.html":
            return quest_log_path(self._config)
        elif remote_name == "journal.html":
            return journal_path(self._config)
        elif remote_name == "shared_config.json":
            return shared_config_path(self._config)
        return os.path.join(active_campaign_dir(self._config), remote_name)

    def initialize(self, credentials) -> bool:
        """Build Drive service and find/create campaign folder.

        Must be called from the UI thread before start().
        Returns True on success.
        """
        try:
            from googleapiclient.discovery import build

            log.info("Building Drive service...")
            self._service = build("drive", "v3", credentials=credentials)
            self._folder_mgr = DriveFolderManager(self._service)

            drive_cfg = campaign_drive_config(self._config)
            folder_id = drive_cfg.get("drive_campaign_folder_id", "")
            log.info("Campaign folder ID from config: %s", folder_id or "(none)")
            if not folder_id:
                cname = active_campaign_name(self._config)
                folder_id = self._folder_mgr.get_or_create_campaign_folder(cname)
                # Save folder_id back into campaigns dict
                cname = active_campaign_name(self._config)
                if "campaigns" not in self._config:
                    self._config["campaigns"] = {}
                if cname not in self._config["campaigns"]:
                    self._config["campaigns"][cname] = {}
                self._config["campaigns"][cname]["drive_campaign_folder_id"] = folder_id
                from .utils import save_config
                save_config(self._config)

            self._file_mgr = DriveFileManager(self._service, folder_id)
            return True
        except Exception as e:
            log.exception("Failed to initialize Drive sync")
            self.error_occurred.emit(f"Erreur d'initialisation Drive: {e}")
            return False

    def start(self):
        """Start periodic polling."""
        if not self._file_mgr:
            return
        self._set_status(SyncStatus.IDLE)
        self._poll_timer.start(_POLL_INTERVAL_MS)
        # Do an immediate poll
        self._poll_remote()

    def stop(self):
        """Stop sync engine."""
        self._poll_timer.stop()
        for timer in self._upload_timers.values():
            timer.stop()
        self._upload_timers.clear()
        self._set_status(SyncStatus.DISABLED)

    def trigger_upload(self, filename: str):
        """Schedule a debounced upload for the given file."""
        if self._status == SyncStatus.DISABLED or not self._file_mgr:
            return
        # Cancel existing timer for this file
        if filename in self._upload_timers:
            self._upload_timers[filename].stop()

        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda fn=filename: self._do_upload(fn))
        timer.start(_UPLOAD_DEBOUNCE_MS)
        self._upload_timers[filename] = timer

    def _do_upload(self, remote_name: str):
        """Execute the actual upload in a worker thread."""
        self._upload_timers.pop(remote_name, None)
        local_path = self._local_path_for(remote_name)
        if not os.path.exists(local_path):
            log.warning("Upload skipped — local file missing: %s", local_path)
            return
        log.info("Uploading %s (%s)", remote_name, local_path)

        self._set_status(SyncStatus.SYNCING)

        thread = QThread()
        worker = _UploadWorker(self._file_mgr, local_path, remote_name)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        entry = (thread, worker)
        worker.finished.connect(lambda fn, meta, e=entry: self._on_upload_done(fn, meta, e))
        worker.error.connect(lambda fn, err, e=entry: self._on_upload_error(fn, err, e))
        self._active_threads.append(entry)
        thread.start()

    def _on_upload_done(self, filename: str, metadata: dict, entry: tuple):
        thread, _worker = entry
        thread.quit()
        thread.wait()
        self._active_threads.remove(entry)

        # Update sync state
        local_path = self._local_path_for(filename)
        self._sync_state[filename] = {
            "local_md5": _local_md5(local_path),
            "remote_modified": metadata.get("modifiedTime", ""),
            "remote_md5": metadata.get("md5Checksum", ""),
            "last_sync": time.time(),
        }
        _save_sync_state(self._sync_state, self._config)
        log.info("Uploaded %s to Drive", filename)

        if not self._active_threads:
            self._set_status(SyncStatus.IDLE)
            self.sync_completed.emit()

    def _on_upload_error(self, filename: str, error: str, entry: tuple):
        thread, _worker = entry
        thread.quit()
        thread.wait()
        self._active_threads.remove(entry)

        log.error("Upload failed for %s: %s", filename, error)
        if "invalid_grant" in error.lower() or "token" in error.lower():
            self._set_status(SyncStatus.ERROR)
            self.error_occurred.emit("Session Drive expirée. Reconnectez-vous dans les paramètres.")
        else:
            self._set_status(SyncStatus.ERROR)
            self.error_occurred.emit(f"Erreur d'upload ({filename}): {error}")

    def _poll_remote(self):
        """Check remote file metadata and download if changed."""
        if not self._file_mgr or self._status == SyncStatus.DISABLED:
            log.debug("Poll skipped: file_mgr=%s status=%s", bool(self._file_mgr), self._status)
            return

        log.info("Polling remote files...")
        filenames = list(SYNCABLE_FILES.values())
        thread = QThread()
        worker = _PollWorker(self._file_mgr, filenames)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        entry = (thread, worker)
        worker.finished.connect(lambda results, e=entry: self._on_poll_done(results, e))
        worker.error.connect(lambda err, e=entry: self._on_poll_error(err, e))
        self._active_threads.append(entry)
        thread.start()

    def _on_poll_done(self, results: dict, entry: tuple):
        thread, _worker = entry
        thread.quit()
        thread.wait()
        self._active_threads.remove(entry)
        log.info("Poll done: %s", {k: ("exists" if v else "missing") for k, v in results.items()})

        for remote_name, remote_meta in results.items():
            if remote_meta is None:
                # File doesn't exist on Drive yet — upload if local copy exists
                local_path = self._local_path_for(remote_name)
                if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
                    self._do_upload(remote_name)
                continue
            direction = self._compute_direction(remote_name, remote_meta)
            if direction == SyncDirection.DOWN:
                self._start_download(remote_name)
            elif direction == SyncDirection.CONFLICT:
                self._handle_conflict(remote_name)
            elif direction == SyncDirection.UP:
                self._do_upload(remote_name)

    def _on_poll_error(self, error: str, entry: tuple):
        thread, _worker = entry
        thread.quit()
        thread.wait()
        self._active_threads.remove(entry)

        if "timeout" in error.lower() or "connection" in error.lower():
            self._set_status(SyncStatus.OFFLINE)
        else:
            log.error("Poll error: %s", error)

    def _compute_direction(self, remote_name: str, remote_meta: dict) -> SyncDirection:
        """Determine sync direction by comparing local/remote state against last sync."""
        state = self._sync_state.get(remote_name, {})
        local_path = self._local_path_for(remote_name)

        current_local_md5 = _local_md5(local_path)
        current_remote_md5 = remote_meta.get("md5Checksum", "")
        current_remote_modified = remote_meta.get("modifiedTime", "")

        last_local_md5 = state.get("local_md5", "")
        last_remote_md5 = state.get("remote_md5", "")

        local_changed = current_local_md5 != last_local_md5 and last_local_md5 != ""
        remote_changed = current_remote_md5 != last_remote_md5 and last_remote_md5 != ""

        # First sync: if we have no state, and the file exists remotely, download it
        if not state:
            if not os.path.exists(local_path) or os.path.getsize(local_path) == 0:
                return SyncDirection.DOWN
            # Both exist, no prior state → conflict
            if current_local_md5 != current_remote_md5:
                return SyncDirection.CONFLICT
            # Same content, just record state
            self._sync_state[remote_name] = {
                "local_md5": current_local_md5,
                "remote_modified": current_remote_modified,
                "remote_md5": current_remote_md5,
                "last_sync": time.time(),
            }
            _save_sync_state(self._sync_state, self._config)
            return SyncDirection.NONE

        if local_changed and remote_changed:
            return SyncDirection.CONFLICT
        if remote_changed:
            return SyncDirection.DOWN
        if local_changed:
            return SyncDirection.UP
        return SyncDirection.NONE

    def _start_download(self, remote_name: str):
        """Download a remote file in a worker thread."""
        local_path = self._local_path_for(remote_name)
        self._set_status(SyncStatus.SYNCING)

        thread = QThread()
        worker = _DownloadWorker(self._file_mgr, remote_name, local_path)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        entry = (thread, worker)
        worker.finished.connect(lambda fn, e=entry: self._on_download_done(fn, e))
        worker.error.connect(lambda fn, err, e=entry: self._on_download_error(fn, err, e))
        self._active_threads.append(entry)
        thread.start()

    def _on_download_done(self, remote_name: str, entry: tuple):
        thread, _worker = entry
        thread.quit()
        thread.wait()
        self._active_threads.remove(entry)

        local_path = self._local_path_for(remote_name)
        remote_meta = self._file_mgr.get_remote_metadata(remote_name)
        self._sync_state[remote_name] = {
            "local_md5": _local_md5(local_path),
            "remote_modified": remote_meta.get("modifiedTime", "") if remote_meta else "",
            "remote_md5": remote_meta.get("md5Checksum", "") if remote_meta else "",
            "last_sync": time.time(),
        }
        _save_sync_state(self._sync_state, self._config)
        log.info("Downloaded %s from Drive", remote_name)

        self.remote_file_updated.emit(remote_name)

        if not self._active_threads:
            self._set_status(SyncStatus.IDLE)
            self.sync_completed.emit()

    def _on_download_error(self, remote_name: str, error: str, entry: tuple):
        thread, _worker = entry
        thread.quit()
        thread.wait()
        self._active_threads.remove(entry)
        log.error("Download failed for %s: %s", remote_name, error)
        self.error_occurred.emit(f"Erreur de téléchargement ({remote_name}): {error}")
        if not self._active_threads:
            self._set_status(SyncStatus.ERROR)

    def _handle_conflict(self, remote_name: str):
        """Handle a conflict by downloading remote content to a temp file, then emitting signal."""
        local_path = self._local_path_for(remote_name)
        temp_path = local_path + ".remote_tmp"

        try:
            self._file_mgr.download_file(remote_name, temp_path)
            with open(local_path, "r", encoding="utf-8") as f:
                local_content = f.read()
            with open(temp_path, "r", encoding="utf-8") as f:
                remote_content = f.read()
            os.remove(temp_path)

            self._set_status(SyncStatus.CONFLICT)
            self.conflict_detected.emit(remote_name, local_content, remote_content)
        except Exception as e:
            log.error("Conflict handling failed for %s: %s", remote_name, e)
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def resolve_conflict(self, remote_name: str, merged_content: str):
        """Write merged content locally and upload to Drive."""
        local_path = self._local_path_for(remote_name)
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(merged_content)
        self.trigger_upload(remote_name)
        self.remote_file_updated.emit(remote_name)

    def cleanup(self):
        """Stop everything and wait for threads."""
        self.stop()
        for thread, _worker in list(self._active_threads):
            thread.quit()
            thread.wait(2000)
        self._active_threads.clear()
