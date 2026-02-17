"""DndLoggerApp — main window."""

import json
import logging
import os
import shutil
import subprocess

from src import __version__

from PySide6.QtCore import QSettings, QTimer, Qt
from PySide6.QtGui import (
    QAction,
    QActionGroup,
    QBrush,
    QColor,
    QFontDatabase,
    QIcon,
    QKeySequence,
    QPalette,
    QPixmap,
    QShortcut,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenuBar,
    QProgressDialog,
    QPushButton,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
)

from .frost_overlay import GoldFiligreeOverlay
from .journal import JournalWidget
from .quest_log import QuestLogWidget
from .session_tab import SessionTab
from .settings import FirstRunWizard, SettingsDialog
from .tts_engine import create_tts_thread
from .tts_overlay import TTSOverlay
from . import themed_dialogs as dlg
from .updater import start_update_check, start_update_download
from .utils import (
    SHARED_CONFIG_KEYS,
    active_campaign_dir,
    active_campaign_name,
    campaign_dir,
    campaign_drive_config,
    format_file_size,
    journal_path,
    list_campaigns,
    load_config,
    project_root,
    quest_log_path,
    resource_path,
    save_config,
    shared_config_path,
)
from .web_panel import DndBeyondBrowser


class _ViewportBgPainter:
    """Event filter that paints a scaled pixmap behind a QTextEdit viewport."""

    def __init__(self, pixmap):
        self._pixmap = pixmap
        self._scaled = None
        self._last_size = None

    def eventFilter(self, obj, event):
        from PySide6.QtCore import QEvent
        if event.type() == QEvent.Type.Paint:
            size = obj.size()
            if size != self._last_size:
                self._scaled = self._pixmap.scaled(
                    size, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self._last_size = size
            from PySide6.QtGui import QPainter
            painter = QPainter(obj)
            painter.drawPixmap(0, 0, self._scaled)
            painter.end()
            # Don't consume — let QTextEdit paint text on top
            return False
        return False


def _install_bg_painter(text_edit, pixmap):
    """Install a background-image painter on a QTextEdit's viewport."""
    from PySide6.QtCore import QObject
    vp = text_edit.viewport()
    # Wrap in QObject so Qt event filter mechanism works
    parent = text_edit
    filter_obj = QObject(parent)
    filter_obj.eventFilter = _ViewportBgPainter(pixmap).eventFilter
    # Keep a reference so it isn't garbage-collected
    text_edit._bg_painter = filter_obj
    vp.installEventFilter(filter_obj)


class CampaignCreationDialog(QDialog):
    """Dialog for creating a new campaign or joining one via Google Drive."""

    def __init__(self, existing_campaigns: list[str], force: bool = False, parent=None):
        super().__init__(parent)
        self._existing = existing_campaigns
        self._force = force
        self._campaign_name = ""
        self._drive_folder_id = ""
        self._auth_thread = None
        self._auth_worker = None
        self.setWindowTitle("Nouvelle campagne")
        self.setMinimumWidth(460)
        self._build_ui()
        if force:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)

    def _build_ui(self):
        layout = QVBoxLayout(self)

        if self._force:
            hint = QLabel("Aucune campagne trouvée.")
            hint.setStyleSheet("color: #d4af37; font-size: 13px;")
            layout.addWidget(hint)
            layout.addSpacing(8)

        # --- Local creation ---
        name_label = QLabel("Nom de la campagne:")
        layout.addWidget(name_label)
        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("Ex: Icewind Dale, Curse of Strahd...")
        layout.addWidget(self._name_edit)

        layout.addSpacing(4)

        create_row = QHBoxLayout()
        create_row.addStretch()
        self._btn_create = QPushButton("Créer")
        self._btn_create.setObjectName("btn_primary")
        self._btn_create.clicked.connect(self._on_create)
        create_row.addWidget(self._btn_create)
        layout.addLayout(create_row)

        layout.addSpacing(12)

        # --- Google Drive section ---
        drive_group = QGroupBox("Google Drive")
        drive_layout = QVBoxLayout(drive_group)

        status_row = QHBoxLayout()
        status_row.addWidget(QLabel("Statut:"))
        self._drive_status_label = QLabel("Non connecté")
        self._drive_status_label.setStyleSheet("color: #8899aa;")
        status_row.addWidget(self._drive_status_label)
        status_row.addStretch()
        self._btn_drive_login = QPushButton("Se connecter")
        self._btn_drive_login.setObjectName("btn_primary")
        self._btn_drive_login.clicked.connect(self._drive_login)
        status_row.addWidget(self._btn_drive_login)
        drive_layout.addLayout(status_row)

        folder_row = QHBoxLayout()
        folder_row.addWidget(QLabel("ID du dossier:"))
        self._folder_id_edit = QLineEdit()
        self._folder_id_edit.setPlaceholderText("Coller l'ID du dossier partagé...")
        folder_row.addWidget(self._folder_id_edit)
        drive_layout.addLayout(folder_row)

        join_row = QHBoxLayout()
        join_row.addStretch()
        self._btn_join = QPushButton("Rejoindre")
        self._btn_join.setObjectName("btn_primary")
        self._btn_join.clicked.connect(self._on_join)
        join_row.addWidget(self._btn_join)
        drive_layout.addLayout(join_row)

        layout.addWidget(drive_group)

        # Status message
        self._status_label = QLabel("")
        self._status_label.setStyleSheet("color: #8899aa; font-size: 11px;")
        self._status_label.setWordWrap(True)
        layout.addWidget(self._status_label)

        if not self._force:
            cancel_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)
            cancel_box.rejected.connect(self.reject)
            layout.addWidget(cancel_box)

        # Initialize Drive status
        self._refresh_drive_status()

    def _on_create(self):
        name = self._name_edit.text().strip()
        if not name:
            self._status_label.setText("Le nom ne peut pas être vide.")
            self._status_label.setStyleSheet("color: #ff6b6b; font-size: 11px;")
            return
        if name in self._existing:
            self._status_label.setText(f'La campagne "{name}" existe déjà.')
            self._status_label.setStyleSheet("color: #ff6b6b; font-size: 11px;")
            return
        self._campaign_name = name
        self._drive_folder_id = ""
        self.accept()

    def _refresh_drive_status(self):
        """Update Drive status label from saved credentials."""
        try:
            from .drive_auth import get_user_email, load_credentials

            creds = load_credentials()
            if creds and creds.valid:
                email = get_user_email(creds)
                self._drive_status_label.setText(email or "Connecté")
                self._drive_status_label.setStyleSheet("color: #7ec83a;")
                self._btn_drive_login.setEnabled(False)
            else:
                self._drive_status_label.setText("Non connecté")
                self._drive_status_label.setStyleSheet("color: #8899aa;")
                self._btn_drive_login.setEnabled(True)
        except ImportError:
            self._drive_status_label.setText("Dépendances Google manquantes")
            self._drive_status_label.setStyleSheet("color: #ff6b6b;")
            self._btn_drive_login.setEnabled(False)
            self._btn_join.setEnabled(False)

    def _drive_login(self):
        """Start OAuth2 login flow."""
        try:
            from .drive_auth import start_auth_flow

            self._btn_drive_login.setEnabled(False)
            self._btn_drive_login.setText("Connexion en cours...")
            self._btn_create.setEnabled(False)
            self._auth_thread, self._auth_worker = start_auth_flow()
            self._auth_worker.auth_completed.connect(self._on_auth_done)
            self._auth_worker.auth_failed.connect(self._on_auth_failed)
            self._auth_thread.start()
        except ImportError:
            dlg.critical(
                self, "Erreur",
                "Installez les dépendances Google:\n"
                "pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib",
            )

    def _on_auth_done(self, creds):
        self._btn_drive_login.setText("Se connecter")
        self._btn_create.setEnabled(True)
        self._refresh_drive_status()
        self._status_label.setText("Connecté ! Collez l'ID du dossier et cliquez Rejoindre.")
        self._status_label.setStyleSheet("color: #7ec83a; font-size: 11px;")

    def _on_auth_failed(self, error: str):
        self._btn_drive_login.setText("Se connecter")
        self._btn_drive_login.setEnabled(True)
        self._btn_create.setEnabled(True)
        self._status_label.setText(f"Échec de connexion: {error}")
        self._status_label.setStyleSheet("color: #ff6b6b; font-size: 11px;")

    def _on_join(self):
        """Resolve folder name from Drive and accept."""
        folder_id = self._folder_id_edit.text().strip()
        if not folder_id:
            self._status_label.setText("Collez l'ID du dossier partagé.")
            self._status_label.setStyleSheet("color: #ff6b6b; font-size: 11px;")
            return

        try:
            from .drive_auth import load_credentials

            creds = load_credentials()
            if not creds:
                self._status_label.setText("Connectez-vous d'abord à Google Drive.")
                self._status_label.setStyleSheet("color: #ff6b6b; font-size: 11px;")
                return

            from googleapiclient.discovery import build

            self._status_label.setText("Résolution du dossier...")
            self._status_label.setStyleSheet("color: #d4af37; font-size: 11px;")
            QApplication.processEvents()

            service = build("drive", "v3", credentials=creds)
            result = service.files().get(fileId=folder_id, fields="name").execute()
            folder_name = result.get("name", "").strip()

            if not folder_name:
                self._status_label.setText("Impossible de résoudre le nom du dossier.")
                self._status_label.setStyleSheet("color: #ff6b6b; font-size: 11px;")
                return

            if folder_name in self._existing:
                self._status_label.setText(f'La campagne "{folder_name}" existe déjà.')
                self._status_label.setStyleSheet("color: #ff6b6b; font-size: 11px;")
                return

            self._campaign_name = folder_name
            self._drive_folder_id = folder_id
            self.accept()
        except ImportError:
            self._status_label.setText("Dépendances Google manquantes.")
            self._status_label.setStyleSheet("color: #ff6b6b; font-size: 11px;")
        except Exception as e:
            self._status_label.setText(f"Erreur Drive: {e}")
            self._status_label.setStyleSheet("color: #ff6b6b; font-size: 11px;")

    def get_result(self) -> tuple[str, str]:
        """Return (campaign_name, drive_folder_id). folder_id is '' for local-only."""
        return self._campaign_name, self._drive_folder_id

    def reject(self):
        if self._force:
            return  # Can't close when force=True
        super().reject()

    def closeEvent(self, event):
        if self._force:
            event.ignore()
        else:
            super().closeEvent(event)


class DndLoggerApp(QMainWindow):
    """Main application window with split layout."""

    def __init__(self):
        super().__init__()
        self._config = load_config()
        self._migrate_to_campaigns()
        self._migrate_shared_config()
        self._ensure_campaign_exists()
        self._current_theme_id = None
        self._theme_meta = None
        self._load_icon()
        self._load_fonts()
        self._load_theme()
        self._migrate_journal()
        self._init_tts()
        self._build_ui()
        self._init_tts_overlay()
        self._init_sync_engine()
        self._add_decorative_overlays()
        # Defer background application so it runs after the window is shown —
        # QSS polish on first show() overrides palette set during __init__.
        QTimer.singleShot(0, self._apply_backgrounds)
        self._build_menu()
        self._restore_geometry()
        self._check_first_run()
        self._update_thread = None
        self._update_worker = None
        self._download_thread = None
        self._download_worker = None
        if self._config.get("auto_update_check", True):
            QTimer.singleShot(3000, self._check_for_updates)

    # ── Migration: flat layout → campaigns/ ─────────────────

    def _migrate_to_campaigns(self):
        """One-time migration: move flat files into campaigns/<name>/."""
        root = project_root()
        campaigns_root = os.path.join(root, "campaigns")
        if os.path.isdir(campaigns_root):
            # Clean up obsolete flat keys that may linger from before migration
            dirty = False
            for old_key in ('drive_sync_enabled', 'drive_campaign_name',
                            'drive_campaign_folder_id', 'sessions_dir',
                            'quest_log_path', 'journal_path'):
                if old_key in self._config:
                    del self._config[old_key]
                    dirty = True
            if dirty:
                save_config(self._config)
            return

        # Check if there are actually legacy files to migrate
        legacy_files = ["quest_log.html", "journal.html", "shared_config.json"]
        has_legacy = any(os.path.exists(os.path.join(root, f)) for f in legacy_files)
        has_legacy = has_legacy or os.path.isdir(os.path.join(root, "sessions"))
        if not has_legacy:
            return  # Fresh install — nothing to migrate

        # Determine campaign name from old config
        campaign_name = self._config.get("drive_campaign_name", "Icewind Dale")

        dest = os.path.join(campaigns_root, campaign_name)
        os.makedirs(dest, exist_ok=True)

        # Move files
        movable_files = [
            "quest_log.html", "quest_log.html.bak",
            "quest_log.html.pre_migration.bak",
            "journal.html", "journal.html.bak",
            "shared_config.json",
            "drive_sync_state.json",
        ]
        for fname in movable_files:
            src = os.path.join(root, fname)
            if os.path.exists(src):
                shutil.move(src, os.path.join(dest, fname))

        # Move sessions dir
        old_sessions = os.path.join(root, "sessions")
        if os.path.isdir(old_sessions):
            shutil.move(old_sessions, os.path.join(dest, "sessions"))

        # Restructure config: move Drive keys into campaigns dict
        old_sync_enabled = self._config.pop("drive_sync_enabled", False)
        old_campaign_name = self._config.pop("drive_campaign_name", "")
        old_folder_id = self._config.pop("drive_campaign_folder_id", "")
        self._config.pop("sessions_dir", None)
        self._config.pop("quest_log_path", None)
        self._config.pop("journal_path", None)

        self._config["active_campaign"] = campaign_name
        self._config["campaigns"] = {
            campaign_name: {
                "drive_sync_enabled": old_sync_enabled,
                "drive_campaign_folder_id": old_folder_id,
            }
        }

        save_config(self._config)
        self._config = load_config()

    def _migrate_shared_config(self):
        """One-time migration: extract shared keys from config.json into shared_config.json."""
        if not active_campaign_name(self._config):
            return  # No campaign yet — will run after campaign is created
        if os.path.exists(shared_config_path(self._config)):
            return
        shared = {k: v for k, v in self._config.items() if k in SHARED_CONFIG_KEYS}
        if shared:
            from .utils import save_shared_config
            save_shared_config(shared, self._config)

    def _ensure_campaign_exists(self):
        """Ensure at least one campaign exists. Prompts for creation if none."""
        campaigns = list_campaigns(self._config)
        active = active_campaign_name(self._config)

        # If campaigns exist and active points to a valid one, nothing to do
        if campaigns and active in campaigns:
            return

        # If campaigns exist but active is invalid, switch to first
        if campaigns:
            self._config["active_campaign"] = campaigns[0]
            save_config(self._config)
            self._config = load_config()
            return

        # No campaigns — force creation
        while True:
            dlg = CampaignCreationDialog(
                existing_campaigns=list_campaigns(self._config),
                force=True,
                parent=None,
            )
            if dlg.exec():
                name, folder_id = dlg.get_result()
                self._create_campaign_from_dialog(name, folder_id)
                break

    def _create_campaign_from_dialog(self, name: str, folder_id: str):
        """Helper: create a campaign from dialog result and switch to it."""
        campaign_dir(name)
        if "campaigns" not in self._config:
            self._config["campaigns"] = {}
        camp_cfg = {}
        if folder_id:
            camp_cfg["drive_sync_enabled"] = True
            camp_cfg["drive_campaign_folder_id"] = folder_id
        self._config["campaigns"][name] = camp_cfg
        self._config["active_campaign"] = name
        save_config(self._config)
        self._config = load_config()

    def _init_sync_engine(self):
        """Initialize Google Drive sync if enabled and credentials exist."""
        import logging
        _log = logging.getLogger("dndlogger.sync")

        self._sync_engine = None
        self._sync_status_label = None

        drive_cfg = campaign_drive_config(self._config)
        if not drive_cfg.get("drive_sync_enabled", False):
            _log.info("Drive sync disabled in campaign config")
            return

        try:
            from .drive_auth import load_credentials
            from .drive_sync import DriveSyncEngine

            creds = load_credentials()
            if not creds:
                _log.warning("No valid Drive credentials — skipping sync")
                return
            _log.info("Drive credentials loaded (token=%s...)", creds.token[:20] if creds.token else "None")

            self._sync_engine = DriveSyncEngine(self._config, parent=self)

            # Connect signals BEFORE initialize so errors are visible
            self._sync_engine.remote_file_updated.connect(self._on_remote_file_updated)
            self._sync_engine.conflict_detected.connect(self._on_conflict_detected)
            self._sync_engine.error_occurred.connect(
                lambda msg: self.statusBar().showMessage(msg, 8000)
            )
            self._sync_engine.status_changed.connect(self._on_sync_status_changed)

            if not self._sync_engine.initialize(creds):
                _log.error("Sync engine initialize() returned False")
                self._sync_engine = None
                return

            _log.info("Sync engine initialized — connecting signals and starting")

            # Connect file_saved signals from editors → trigger upload
            self.journal.file_saved.connect(self._on_editor_file_saved)
            self.quest_log.file_saved.connect(self._on_editor_file_saved)

            self._sync_engine.start()
            _log.info("Sync engine started")
        except ImportError as e:
            _log.warning("Google API packages not installed: %s", e)
        except Exception as e:
            _log.exception("Unexpected error in _init_sync_engine: %s", e)

    def _on_editor_file_saved(self, file_path: str):
        """Route a file save to the sync engine with the right remote name."""
        if not self._sync_engine:
            return
        basename = os.path.basename(file_path)
        from .drive_sync import SYNCABLE_FILES
        if basename in SYNCABLE_FILES:
            self._sync_engine.trigger_upload(basename)

    def _on_remote_file_updated(self, remote_name: str):
        """Reload the appropriate editor when a remote file is downloaded."""
        if remote_name == "quest_log.html":
            self.quest_log.reload_from_disk()
        elif remote_name == "journal.html":
            self.journal.reload_from_disk()
        elif remote_name == "shared_config.json":
            # Reload config and push to child widgets
            self._config = load_config()
            self._refresh_config()

    def _on_conflict_detected(self, filename: str, local_content: str, remote_content: str):
        """Show the conflict resolution dialog."""
        try:
            from .sync_conflict_dialog import SyncConflictDialog

            dlg = SyncConflictDialog(filename, local_content, remote_content, parent=self)
            if dlg.exec():
                merged = dlg.get_merged_content()
                self._sync_engine.resolve_conflict(filename, merged)
        except ImportError:
            pass

    def _on_sync_status_changed(self, status):
        """Update the sync status indicator in the status bar."""
        if not self._sync_status_label:
            return
        if status is None:
            self._sync_status_label.setText("")
            return
        from .drive_sync import SyncStatus
        labels = {
            SyncStatus.DISABLED: ("Drive: désactivé", "#8899aa"),
            SyncStatus.IDLE: ("Drive: synchronisé", "#7ec83a"),
            SyncStatus.SYNCING: ("Drive: synchronisation...", "#d4af37"),
            SyncStatus.CONFLICT: ("Drive: conflit détecté", "#ff6b6b"),
            SyncStatus.ERROR: ("Drive: erreur", "#ff6b6b"),
            SyncStatus.OFFLINE: ("Drive: hors ligne", "#8899aa"),
        }
        text, color = labels.get(status, ("Drive: ?", "#8899aa"))
        self._sync_status_label.setText(text)
        self._sync_status_label.setStyleSheet(f"color: {color}; padding: 0 8px;")

    def _load_icon(self):
        """Set the D20 window/taskbar icon."""
        icon_path = resource_path("assets/images/app/icon.png")
        if not os.path.exists(icon_path):
            icon_path = resource_path("assets/images/app/icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _load_fonts(self):
        """Load custom fonts from assets."""
        fonts_dir = resource_path("assets/fonts")
        if os.path.isdir(fonts_dir):
            for fname in os.listdir(fonts_dir):
                if fname.lower().endswith((".ttf", ".otf")):
                    QFontDatabase.addApplicationFont(os.path.join(fonts_dir, fname))

    # ── Theme system ─────────────────────────────────────────

    # Keyword → theme_id mapping for fuzzy resolution (includes French equivalents)
    _THEME_KEYWORDS = {
        "icewind":       "icewind_dale",
        "frostmaiden":   "icewind_dale",
        "auril":         "icewind_dale",
        "givre":         "icewind_dale",
        "strahd":        "curse_of_strahd",
        "barovia":       "curse_of_strahd",
        "ravenloft":     "curse_of_strahd",
        "avernus":       "descent_into_avernus",
        "averné":        "descent_into_avernus",
        "enfer":         "descent_into_avernus",
        "zariel":        "descent_into_avernus",
        "annihilation":  "tomb_of_annihilation",
        "chult":         "tomb_of_annihilation",
        "tombeau":       "tomb_of_annihilation",
        "acererak":      "tomb_of_annihilation",
        "storm":         "storm_kings_thunder",
        "géant":         "storm_kings_thunder",
        "thunder":       "storm_kings_thunder",
        "waterdeep":     "waterdeep_dragon_heist",
        "eauprofonde":   "waterdeep_dragon_heist",
        "dragon heist":  "waterdeep_dragon_heist",
        "abyss":         "out_of_the_abyss",
        "abîme":         "out_of_the_abyss",
        "underdark":     "out_of_the_abyss",
        "outreterre":    "out_of_the_abyss",
    }

    def _load_theme_meta(self) -> dict:
        """Load theme_meta.json if available."""
        if self._theme_meta is not None:
            return self._theme_meta
        meta_path = resource_path("assets/styles/theme_meta.json")
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    self._theme_meta = json.load(f)
            except (json.JSONDecodeError, OSError):
                self._theme_meta = {}
        else:
            self._theme_meta = {}
        return self._theme_meta

    def _available_themes(self) -> dict:
        """Return dict of {theme_id: theme_data} from meta."""
        meta = self._load_theme_meta()
        return {k: v for k, v in meta.get("themes", {}).items() if k != "_fallback"}

    def _resolve_theme(self) -> str | None:
        """Resolve theme for the active campaign using 3-tier priority.

        1. Explicit choice in campaign config
        2. Fuzzy keyword matching on campaign name
        3. None (caller should show picker)
        """
        active = active_campaign_name(self._config)
        available = self._available_themes()
        if not available:
            return None

        # Tier 1: explicit choice stored in campaign config
        camp_cfg = self._config.get("campaigns", {}).get(active, {})
        explicit = camp_cfg.get("theme")
        if explicit and explicit in available:
            return explicit

        # Tier 2: fuzzy keyword matching
        name_lower = active.lower()
        for keyword, theme_id in self._THEME_KEYWORDS.items():
            if keyword in name_lower and theme_id in available:
                return theme_id

        # Tier 3: no match
        return None

    def _load_theme(self, theme_id: str | None = None):
        """Load a theme by ID or auto-resolve. Falls back to icewind_dale.qss."""
        if theme_id is None:
            theme_id = self._resolve_theme()

        # Invalidate cached meta so fresh data is used for overlay/image lookups
        self._theme_meta = None
        meta = self._load_theme_meta()
        themes = meta.get("themes", {})

        # Try loading the requested theme's QSS
        if theme_id and theme_id in themes:
            qss_file = themes[theme_id].get("qss_file", f"{theme_id}.qss")
            qss_path = resource_path(f"assets/styles/{qss_file}")
            if os.path.exists(qss_path):
                with open(qss_path, "r", encoding="utf-8") as f:
                    self.setStyleSheet(f.read())
                self._current_theme_id = theme_id
                return

        # Fallback: use icewind_dale.qss
        qss_path = resource_path("assets/styles/icewind_dale.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        self._current_theme_id = theme_id or "icewind_dale"

    def _show_theme_picker(self) -> str | None:
        """Show a dialog to pick a theme. Returns theme_id or None."""
        available = self._available_themes()
        if not available:
            return None

        dlg = QDialog(self)
        dlg.setWindowTitle("Choisir un thème")
        dlg.setMinimumWidth(350)
        layout = QVBoxLayout(dlg)

        label = QLabel("Aucun thème automatique trouvé pour cette campagne.\nChoisissez un thème visuel:")
        layout.addWidget(label)

        combo = QComboBox()
        theme_ids = []
        for tid, tdata in sorted(available.items(), key=lambda x: x[1].get("display_name", "")):
            combo.addItem(tdata.get("display_name", tid))
            theme_ids.append(tid)
        layout.addWidget(combo)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)

        if dlg.exec() == QDialog.DialogCode.Accepted and theme_ids:
            return theme_ids[combo.currentIndex()]
        return None

    def _switch_theme(self, theme_id: str):
        """Switch to a specific theme and save choice to campaign config."""
        self._load_theme(theme_id)
        self._apply_backgrounds()
        self._update_session_icon()
        self._update_overlay_colors()

        # Save choice to campaign config
        active = active_campaign_name(self._config)
        if active:
            self._config.setdefault("campaigns", {}).setdefault(active, {})["theme"] = theme_id
            save_config(self._config)

        self._rebuild_campaign_menu()

    def _update_session_icon(self):
        """Set the Session tab icon matching the current theme."""
        tid = self._current_theme_id or "icewind_dale"
        icon_path = resource_path(f"assets/images/tabs/tab_icon_session_{tid}.png")
        if os.path.exists(icon_path):
            self.right_tabs.setTabIcon(self._session_tab_index, QIcon(icon_path))

    def _update_overlay_colors(self):
        """Push theme overlay colors and particle type to all decorative overlays."""
        meta = self._load_theme_meta()
        themes = meta.get("themes", {})
        theme_data = themes.get(self._current_theme_id, {})
        overlays = theme_data.get("overlays", {})

        # Filigree color
        fc = overlays.get("filigree_color", [201, 168, 50, 100])
        filigree_qcolor = QColor(*fc)
        for attr in ("_journal_filigree", "_quest_filigree", "_session_filigree"):
            overlay = getattr(self, attr, None)
            if overlay:
                overlay.set_color(filigree_qcolor)

        # Particle type + color
        snow = getattr(self.session_tab, "_snow_overlay", None)
        if snow:
            pt = overlays.get("particle_type", "snow")
            snow.set_particle_type(pt)
            pc = overlays.get("particle_color", [220, 240, 255])
            snow.set_particle_color(pc)

        # Aurora tones
        at = overlays.get("aurora_tones", [[10, 25, 35], [20, 15, 45], [15, 20, 35]])
        aurora = getattr(self.session_tab, "_aurora_overlay", None)
        if aurora:
            aurora.set_aurora_tones(at)

        # Divider accent — use the theme's accent_gold equivalent
        palette = theme_data.get("palette", {})
        accent_hex = palette.get("accent_gold", "#c9a832")
        accent_color = QColor(accent_hex)
        self.session_tab.set_divider_accent(accent_color)

    def _init_tts(self):
        """Initialize a shared TTS engine for all widgets."""
        self._tts_thread, self._tts_engine = create_tts_thread()
        self._tts_engine.error.connect(self._on_tts_error)
        self._tts_thread.start()
        self._tts_overlay = None  # created after UI is built
        # Escape key stops TTS playback
        self._tts_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        self._tts_shortcut.activated.connect(self._stop_tts)

    def _init_tts_overlay(self):
        """Create the TTS overlay and wire it to engine signals."""
        self._tts_overlay = TTSOverlay(self.right_tabs)
        self._tts_engine.started.connect(self._tts_overlay.show_overlay)
        self._tts_engine.finished.connect(self._tts_overlay.hide_overlay)
        self._tts_engine.paused.connect(lambda: self._tts_overlay.set_paused(True))
        self._tts_engine.resumed.connect(lambda: self._tts_overlay.set_paused(False))
        self._tts_overlay.pause_toggled.connect(self._toggle_tts_pause)
        self._tts_overlay.stop_requested.connect(self._stop_tts)

    def _toggle_tts_pause(self):
        """Toggle TTS pause / resume."""
        if not self._tts_engine:
            return
        if self._tts_engine.is_paused:
            self._tts_engine.resume()
        else:
            self._tts_engine.pause()

    def _stop_tts(self):
        """Stop TTS playback on Escape key, unless a search bar is open."""
        from PySide6.QtWidgets import QApplication
        from .rich_editor import _SearchLineEdit
        focused = QApplication.focusWidget()
        if isinstance(focused, _SearchLineEdit):
            focused._editor_widget._close_search()
            return
        if self._tts_engine:
            self._tts_engine.stop()
        if self._tts_overlay:
            self._tts_overlay.hide_overlay()

    def _on_tts_error(self, msg: str):
        """Show TTS errors in the status bar."""
        self.statusBar().showMessage(msg, 5000)

    def _migrate_journal(self):
        """One-time migration: copy existing quest log content to journal."""
        j_path = journal_path(self._config)
        ql_path = quest_log_path(self._config)

        if os.path.exists(j_path):
            return  # Already migrated

        if not os.path.exists(ql_path):
            return  # Nothing to migrate

        # Check if quest log has session entries (contains "Session du")
        try:
            with open(ql_path, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError:
            return

        if "Session du" in content:
            # Copy quest log content to journal
            try:
                shutil.copy2(ql_path, j_path)
            except OSError:
                return
            # Reset quest log to new default (will happen naturally when
            # QuestLogWidget loads and finds no file after we remove the old one)
            try:
                bak = ql_path + ".pre_migration.bak"
                shutil.copy2(ql_path, bak)
                os.remove(ql_path)
            except OSError:
                pass

    def _apply_backgrounds(self):
        """Apply background textures to widgets."""
        # Main window background — theme-specific
        tid = self._current_theme_id or "icewind_dale"
        bg_path = resource_path(f"assets/images/backgrounds/bg_{tid}.png")
        if os.path.exists(bg_path):
            palette = self.palette()
            bg_pix = QPixmap(bg_path)
            if not bg_pix.isNull():
                palette.setBrush(QPalette.ColorRole.Window, QBrush(bg_pix))
                self.setPalette(palette)
                self.setAutoFillBackground(True)

        # Parchment texture on journal and quest log editors
        parch_path = resource_path("assets/images/textures/parchment_warm.png")
        if os.path.exists(parch_path):
            parch_pix = QPixmap(parch_path)
            if not parch_pix.isNull():
                for editor in (self.journal.editor, self.quest_log.editor):
                    _install_bg_painter(editor, parch_pix)

    def _add_decorative_overlays(self):
        """Add gold filigree corner decorations to key panels."""
        self._journal_filigree = GoldFiligreeOverlay(self.journal)
        self._quest_filigree = GoldFiligreeOverlay(self.quest_log)
        self._session_filigree = GoldFiligreeOverlay(self.session_tab)
        self._update_overlay_colors()

    def _build_ui(self):
        cname = active_campaign_name(self._config)
        self.setWindowTitle(f"{cname} \u2014 DnD Logger v{__version__}")
        self.setMinimumSize(1200, 700)

        # Main splitter: left (browser) | right (tabs)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel: D&D Beyond browser
        self.browser = DndBeyondBrowser()
        self.splitter.addWidget(self.browser)

        # Right panel: tabs
        self.right_tabs = QTabWidget()

        self.journal = JournalWidget(self._config)
        self.journal.set_tts_engine(self._tts_engine)
        self.quest_log = QuestLogWidget(self._config)
        self.quest_log.set_tts_engine(self._tts_engine)

        # Tab icons
        quill_icon_path = resource_path("assets/images/tabs/tab_icon_questlog.png")

        # Journal tab (first)
        if os.path.exists(quill_icon_path):
            self.right_tabs.addTab(self.journal, QIcon(quill_icon_path), "Journal")
        else:
            self.right_tabs.addTab(self.journal, "Journal")

        # Quest Log tab (second)
        if os.path.exists(quill_icon_path):
            self.right_tabs.addTab(self.quest_log, QIcon(quill_icon_path), "Quest Log")
        else:
            self.right_tabs.addTab(self.quest_log, "Quest Log")

        # Session tab (third)
        self.session_tab = SessionTab(
            self._config,
            journal_widget=self.journal,
            quest_log_widget=self.quest_log,
            tts_engine=self._tts_engine,
        )
        self.right_tabs.addTab(self.session_tab, "Session")
        self._session_tab_index = self.right_tabs.indexOf(self.session_tab)
        self._update_session_icon()

        self.splitter.addWidget(self.right_tabs)

        # 55/45 split
        self.splitter.setSizes([600, 500])

        self.setCentralWidget(self.splitter)

        # Sync status label in status bar
        self._sync_status_label = QLabel("")
        self.statusBar().addPermanentWidget(self._sync_status_label)

    def _build_menu(self):
        menu_bar = self.menuBar()

        # Fichier menu
        file_menu = menu_bar.addMenu("Fichier")

        settings_action = QAction("Paramètres...", self)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.triggered.connect(self._open_settings)
        file_menu.addAction(settings_action)

        update_action = QAction("Vérifier les mises à jour...", self)
        update_action.triggered.connect(self._manual_update_check)
        file_menu.addAction(update_action)

        file_menu.addSeparator()

        save_action = QAction("Sauvegarder", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self._save_active_editor)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        quit_action = QAction("Quitter", self)
        quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Campaign menu
        self._campaign_menu = menu_bar.addMenu("Campagne")
        self._rebuild_campaign_menu()

        # Session menu
        session_menu = menu_bar.addMenu("Session")

        record_action = QAction("Enregistrer / Arrêter", self)
        record_action.setShortcut(QKeySequence("Ctrl+R"))
        record_action.triggered.connect(self._toggle_recording)
        session_menu.addAction(record_action)

    def _rebuild_campaign_menu(self):
        """Rebuild the Campaign menu with current campaigns."""
        self._campaign_menu.clear()
        active = active_campaign_name(self._config)
        campaigns = list_campaigns(self._config)

        for name in campaigns:
            action = QAction(name, self)
            action.setCheckable(True)
            action.setChecked(name == active)
            action.triggered.connect(lambda checked, n=name: self._switch_campaign(n))
            self._campaign_menu.addAction(action)

        self._campaign_menu.addSeparator()

        new_action = QAction("Nouvelle campagne...", self)
        new_action.triggered.connect(self._new_campaign)
        self._campaign_menu.addAction(new_action)

        delete_action = QAction("Supprimer la campagne...", self)
        delete_action.triggered.connect(self._delete_campaign)
        self._campaign_menu.addAction(delete_action)

        restore_action = QAction("Restaurer une campagne...", self)
        restore_action.triggered.connect(self._restore_campaign)
        self._campaign_menu.addAction(restore_action)

        # Theme submenu
        available = self._available_themes()
        if available:
            self._campaign_menu.addSeparator()
            theme_menu = self._campaign_menu.addMenu("Thème")
            theme_group = QActionGroup(theme_menu)
            theme_group.setExclusive(True)
            for tid, tdata in sorted(available.items(), key=lambda x: x[1].get("display_name", "")):
                action = QAction(tdata.get("display_name", tid), theme_menu)
                action.setCheckable(True)
                action.setChecked(tid == self._current_theme_id)
                action.triggered.connect(lambda checked, t=tid: self._switch_theme(t))
                theme_group.addAction(action)
                theme_menu.addAction(action)

    def _new_campaign(self):
        """Create a new campaign via the creation dialog."""
        dlg = CampaignCreationDialog(
            existing_campaigns=list_campaigns(self._config),
            force=False,
            parent=self,
        )
        if dlg.exec():
            name, folder_id = dlg.get_result()
            self._create_campaign_from_dialog(name, folder_id)
            self._switch_campaign(name)

    def _delete_campaign(self):
        """Delete a campaign (move to _trash/). Allows deleting any campaign."""
        active = active_campaign_name(self._config)
        campaigns = list_campaigns(self._config)
        if not campaigns:
            return

        name, ok = dlg.get_item(
            self, "Supprimer une campagne",
            "Choisissez la campagne à supprimer :", campaigns, 0, False
        )
        if not ok:
            return

        if not dlg.question(
            self, "Confirmer la suppression",
            f"Supprimer la campagne \"{name}\" ?\n"
            "Les fichiers seront déplacés dans campaigns/_trash/.",
        ):
            return

        # Save editors if deleting the active campaign
        if name == active:
            self.journal.save()
            self.quest_log.save()
            if self._sync_engine:
                self._sync_engine.cleanup()
                self._sync_engine = None
                self._on_sync_status_changed(None)

        # Move to _trash/
        root = project_root()
        trash_dir = os.path.join(root, "campaigns", "_trash")
        os.makedirs(trash_dir, exist_ok=True)
        src = os.path.join(root, "campaigns", name)
        dst = os.path.join(trash_dir, name)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.move(src, dst)

        # Remove from config
        self._config.get("campaigns", {}).pop(name, None)
        save_config(self._config)

        remaining = list_campaigns(self._config)
        if name == active:
            if remaining:
                self._switch_campaign(remaining[0])
            else:
                # No campaigns left — force creation
                self._ensure_campaign_exists()
                self._switch_campaign(active_campaign_name(self._config))
        else:
            self._rebuild_campaign_menu()

    def _restore_campaign(self):
        """Restore a previously deleted campaign from _trash/."""
        trash_dir = os.path.join(project_root(), "campaigns", "_trash")
        if not os.path.isdir(trash_dir):
            dlg.information(self, "Restaurer", "Aucune campagne archivée.")
            return
        trashed = sorted(
            d for d in os.listdir(trash_dir)
            if os.path.isdir(os.path.join(trash_dir, d))
        )
        if not trashed:
            dlg.information(self, "Restaurer", "Aucune campagne archivée.")
            return

        name, ok = dlg.get_item(
            self, "Restaurer une campagne",
            "Choisissez la campagne à restaurer :", trashed, 0, False
        )
        if not ok:
            return

        src = os.path.join(trash_dir, name)
        dst = os.path.join(project_root(), "campaigns", name)
        shutil.move(src, dst)

        self._config.setdefault("campaigns", {})[name] = {}
        save_config(self._config)
        self._switch_campaign(name)

    def _switch_campaign(self, name: str):
        """Switch to a different campaign."""
        if name == active_campaign_name(self._config):
            self._rebuild_campaign_menu()
            return

        # Save current editors
        self.journal.save()
        self.quest_log.save()

        # Stop recording if active
        rec = self.session_tab._recorder
        if rec.is_recording:
            self.session_tab._stop_recording()

        # Stop sync
        if self._sync_engine:
            self._sync_engine.cleanup()
            self._sync_engine = None
            self._on_sync_status_changed(None)

        # Update config
        self._config["active_campaign"] = name
        save_config(self._config)
        self._config = load_config()

        # Update window title
        self.setWindowTitle(f"{name} \u2014 DnD Logger v{__version__}")

        # Switch editor files
        from .quest_log import _default_quest_log_html
        from .journal import _default_journal_html
        self.quest_log.switch_file(
            quest_log_path(self._config),
            _default_quest_log_html(name),
        )
        self.journal.switch_file(
            journal_path(self._config),
            _default_journal_html(name),
        )

        # Refresh child config
        self._refresh_config()

        # Switch theme for new campaign
        theme_id = self._resolve_theme()
        if theme_id is None and self._available_themes():
            theme_id = self._show_theme_picker()
            if theme_id:
                # Save the user's choice
                self._config.setdefault("campaigns", {}).setdefault(name, {})["theme"] = theme_id
                save_config(self._config)
                self._config = load_config()
        self._load_theme(theme_id)
        self._apply_backgrounds()
        self._update_session_icon()
        self._update_overlay_colors()

        # Restart sync if campaign has it enabled
        self._init_sync_engine()

        # Rebuild menu
        self._rebuild_campaign_menu()

    def _save_active_editor(self):
        """Save whichever editor tab is currently active."""
        current = self.right_tabs.currentWidget()
        if current is self.journal:
            self.journal.save()
        elif current is self.quest_log:
            self.quest_log.save()

    def _check_first_run(self):
        """Show first-run wizard if API key is empty."""
        if not self._config.get("api_key"):
            wizard = FirstRunWizard(self._config, self)
            if wizard.exec():
                self._config = wizard.get_config()
                self._refresh_config()

    def _open_settings(self):
        drive_cfg = campaign_drive_config(self._config)
        was_sync_enabled = drive_cfg.get("drive_sync_enabled", False)
        dlg = SettingsDialog(self._config, self)
        if dlg.exec():
            self._config = dlg.get_config()
            self._refresh_config()
            # (Re)start or stop sync engine based on settings change
            new_drive_cfg = campaign_drive_config(self._config)
            now_sync_enabled = new_drive_cfg.get("drive_sync_enabled", False)
            if now_sync_enabled and not self._sync_engine:
                self._init_sync_engine()
            elif not now_sync_enabled and self._sync_engine:
                self._sync_engine.cleanup()
                self._sync_engine = None
                self._on_sync_status_changed(None)

    def _refresh_config(self):
        """Push updated config to child widgets."""
        self.session_tab.update_config(self._config)
        # Trigger shared_config upload if sync is active
        if self._sync_engine:
            self._sync_engine.trigger_upload("shared_config.json")

    def _toggle_recording(self):
        """Toggle recording from keyboard shortcut."""
        rec = self.session_tab._recorder
        if rec.is_recording:
            self.session_tab._stop_recording()
        else:
            self.session_tab._start_recording()
        # Switch to Session tab
        self.right_tabs.setCurrentWidget(self.session_tab)

    # ── Auto-update ────────────────────────────────────────

    def _check_for_updates(self):
        """Start a background update check (silent on error)."""
        self._cleanup_update_thread()
        self._update_thread, self._update_worker = start_update_check()
        self._update_worker.update_available.connect(self._on_update_available)
        self._update_worker.no_update.connect(self._on_update_thread_done)
        self._update_worker.error.connect(self._on_update_check_error)
        self._update_thread.start()

    def _manual_update_check(self):
        """Manual update check — shows dialogs for all outcomes."""
        self._cleanup_update_thread()
        self._update_thread, self._update_worker = start_update_check()
        self._update_worker.update_available.connect(self._on_update_available)
        self._update_worker.no_update.connect(self._on_no_update)
        self._update_worker.error.connect(
            lambda msg: dlg.warning(
                self, "Mise à jour",
                f"Impossible de vérifier les mises à jour.\n{msg}",
            )
        )
        self._update_worker.no_update.connect(self._on_update_thread_done)
        self._update_worker.error.connect(self._on_update_thread_done)
        self._update_thread.start()

    def _on_update_available(self, tag, name, url, body):
        self._on_update_thread_done()

        dlg = QDialog(self)
        dlg.setWindowTitle("Mise à jour disponible")
        dlg.setFixedWidth(400)

        layout = QVBoxLayout(dlg)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 16)

        title = QLabel(f"Version {tag} disponible !")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        if name and name != tag:
            subtitle = QLabel(name)
            subtitle.setWordWrap(True)
            layout.addWidget(subtitle)

        if body:
            from PySide6.QtWidgets import QTextEdit
            details_text = QTextEdit()
            details_text.setReadOnly(True)
            details_text.setPlainText(body)
            details_text.setMaximumHeight(150)
            details_text.setVisible(False)

            btn_details = QPushButton("Détails ▸")
            btn_details.setFlat(True)
            btn_details.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_details.setStyleSheet(
                "text-align: left; padding: 0; border: none; "
                "color: #5a9bc8; font-size: 12px;"
            )

            def _toggle_details():
                visible = not details_text.isVisible()
                details_text.setVisible(visible)
                btn_details.setText("Détails ▾" if visible else "Détails ▸")
                dlg.adjustSize()

            btn_details.clicked.connect(_toggle_details)
            layout.addWidget(btn_details)
            layout.addWidget(details_text)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        btn_later = QPushButton("Plus tard")
        btn_download = QPushButton("Télécharger et installer")
        btn_download.setObjectName("btn_gold")
        btn_row.addStretch()
        btn_row.addWidget(btn_later)
        btn_row.addWidget(btn_download)
        layout.addLayout(btn_row)

        btn_later.clicked.connect(dlg.reject)
        btn_download.clicked.connect(dlg.accept)

        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._start_update_download(url)

    def _on_no_update(self):
        dlg.information(
            self, "Mise à jour",
            f"Vous utilisez la dernière version (v{__version__}).",
        )

    def _on_update_check_error(self, msg):
        log = logging.getLogger(__name__)
        log.warning("Update check failed: %s", msg)
        self._on_update_thread_done()

    def _on_update_thread_done(self):
        if self._update_thread and self._update_thread.isRunning():
            self._update_thread.quit()
            self._update_thread.wait(2000)
        self._update_thread = None
        self._update_worker = None

    def _start_update_download(self, url):
        self._cleanup_download_thread()
        self._download_thread, self._download_worker = start_update_download(url)

        self._progress_dlg = QProgressDialog(
            "Téléchargement de la mise à jour...", "Annuler", 0, 100, self
        )
        self._progress_dlg.setWindowTitle("Mise à jour")
        self._progress_dlg.setWindowModality(Qt.WindowModality.WindowModal)
        self._progress_dlg.setMinimumDuration(0)
        self._progress_dlg.canceled.connect(self._download_worker.cancel)

        self._download_worker.progress.connect(self._on_download_progress)
        self._download_worker.completed.connect(self._on_download_completed)
        self._download_worker.error.connect(self._on_download_error)
        self._download_thread.start()

    def _on_download_progress(self, downloaded, total):
        if total > 0:
            self._progress_dlg.setMaximum(total)
            self._progress_dlg.setValue(downloaded)
            self._progress_dlg.setLabelText(
                f"Téléchargement... {format_file_size(downloaded)} / {format_file_size(total)}"
            )
        else:
            self._progress_dlg.setMaximum(0)
            self._progress_dlg.setLabelText(
                f"Téléchargement... {format_file_size(downloaded)}"
            )

    def _on_download_completed(self, path):
        self._progress_dlg.close()
        self._cleanup_download_thread()
        if dlg.question(
            self, "Mise à jour",
            "Téléchargement terminé.\n"
            "L'application va se fermer pour installer la mise à jour.\n\n"
            "Continuer ?",
        ):
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            DETACHED_PROCESS = 0x00000008
            subprocess.Popen(
                [path, "/SILENT", "/RESTARTAPPLICATIONS"],
                creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
                close_fds=True,
            )
            self.close()

    def _on_download_error(self, msg):
        self._progress_dlg.close()
        self._cleanup_download_thread()
        dlg.warning(
            self, "Mise à jour",
            f"Erreur lors du téléchargement.\n{msg}",
        )

    def _cleanup_update_thread(self):
        if self._update_thread and self._update_thread.isRunning():
            self._update_thread.quit()
            self._update_thread.wait(2000)
        self._update_thread = None
        self._update_worker = None

    def _cleanup_download_thread(self):
        if self._download_worker:
            self._download_worker.cancel()
        if self._download_thread and self._download_thread.isRunning():
            self._download_thread.quit()
            self._download_thread.wait(2000)
        self._download_thread = None
        self._download_worker = None

    def _restore_geometry(self):
        """Restore window size/position from QSettings."""
        settings = QSettings("DnD Logger", "DnD Logger")
        geo = settings.value("geometry")
        if geo:
            self.restoreGeometry(geo)
        state = settings.value("windowState")
        if state:
            self.restoreState(state)

    def _save_geometry(self):
        """Save window size/position."""
        settings = QSettings("DnD Logger", "DnD Logger")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())

    def closeEvent(self, event):
        """Clean up on exit."""
        self._save_geometry()
        self.journal.save()
        self.quest_log.save()
        self.session_tab.cleanup()
        self.browser.cleanup()
        # Shut down update threads
        self._cleanup_update_thread()
        self._cleanup_download_thread()
        # Shut down sync engine
        if self._sync_engine:
            self._sync_engine.cleanup()
        # Shut down shared TTS
        if self._tts_engine:
            self._tts_engine.stop()
        if self._tts_thread and self._tts_thread.isRunning():
            self._tts_thread.quit()
            self._tts_thread.wait(2000)
        # Give QWebEngine a moment to flush cookies/storage to disk
        from PySide6.QtCore import QElapsedTimer

        timer = QElapsedTimer()
        timer.start()
        app = QApplication.instance()
        while timer.elapsed() < 500:
            if app:
                app.processEvents()
        event.accept()
