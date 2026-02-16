"""DndLoggerApp — main window."""

import logging
import os
import shutil
import subprocess

from src import __version__

from PyQt6.QtCore import QSettings, QTimer, Qt
from PyQt6.QtGui import (
    QAction,
    QBrush,
    QFontDatabase,
    QIcon,
    QKeySequence,
    QPalette,
    QPixmap,
    QShortcut,
)
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenuBar,
    QMessageBox,
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

        name_label = QLabel("Nom de la campagne:")
        layout.addWidget(name_label)
        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("Ex: Icewind Dale, Curse of Strahd...")
        layout.addWidget(self._name_edit)

        layout.addSpacing(12)

        btn_row = QHBoxLayout()
        self._btn_create = QPushButton("Créer")
        self._btn_create.setObjectName("btn_primary")
        self._btn_create.clicked.connect(self._on_create)
        btn_row.addWidget(self._btn_create)

        self._btn_drive = QPushButton("Rejoindre via Google Drive")
        self._btn_drive.clicked.connect(self._on_drive_join)
        btn_row.addWidget(self._btn_drive)
        layout.addLayout(btn_row)

        self._status_label = QLabel("")
        self._status_label.setStyleSheet("color: #8899aa; font-size: 11px;")
        self._status_label.setWordWrap(True)
        layout.addWidget(self._status_label)

        if not self._force:
            cancel_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)
            cancel_box.rejected.connect(self.reject)
            layout.addWidget(cancel_box)

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

    def _on_drive_join(self):
        try:
            from .drive_auth import load_credentials, start_auth_flow
        except ImportError:
            QMessageBox.critical(
                self, "Erreur",
                "Installez les dépendances Google:\n"
                "pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib",
            )
            return

        creds = load_credentials()
        if not creds:
            self._status_label.setText("Connexion en cours...")
            self._status_label.setStyleSheet("color: #d4af37; font-size: 11px;")
            self._btn_drive.setEnabled(False)
            self._btn_create.setEnabled(False)
            self._auth_thread, self._auth_worker = start_auth_flow()
            self._auth_worker.auth_completed.connect(self._on_auth_done)
            self._auth_worker.auth_failed.connect(self._on_auth_failed)
            self._auth_thread.start()
            return

        self._prompt_folder_id(creds)

    def _on_auth_done(self, creds):
        self._btn_drive.setEnabled(True)
        self._btn_create.setEnabled(True)
        self._status_label.setText("Connecté ! Entrez l'ID du dossier.")
        self._status_label.setStyleSheet("color: #7ec83a; font-size: 11px;")
        self._prompt_folder_id(creds)

    def _on_auth_failed(self, error: str):
        self._btn_drive.setEnabled(True)
        self._btn_create.setEnabled(True)
        self._status_label.setText(f"Échec de connexion: {error}")
        self._status_label.setStyleSheet("color: #ff6b6b; font-size: 11px;")

    def _prompt_folder_id(self, creds):
        folder_id, ok = QInputDialog.getText(
            self, "Rejoindre via Google Drive",
            "ID du dossier partagé Google Drive:"
        )
        if not ok or not folder_id.strip():
            self._status_label.setText("")
            return
        folder_id = folder_id.strip()

        try:
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
        self._load_icon()
        self._load_fonts()
        self._load_stylesheet()
        self._migrate_journal()
        self._init_tts()
        self._build_ui()
        self._init_tts_overlay()
        self._init_sync_engine()
        self._apply_backgrounds()
        self._add_decorative_overlays()
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
        icon_path = resource_path("assets/images/icon.png")
        if not os.path.exists(icon_path):
            icon_path = resource_path("assets/images/icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _load_fonts(self):
        """Load custom fonts from assets."""
        fonts_dir = resource_path("assets/fonts")
        if os.path.isdir(fonts_dir):
            for fname in os.listdir(fonts_dir):
                if fname.lower().endswith((".ttf", ".otf")):
                    QFontDatabase.addApplicationFont(os.path.join(fonts_dir, fname))

    def _load_stylesheet(self):
        """Load the QSS theme."""
        qss_path = resource_path("assets/styles/icewind.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

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
        from PyQt6.QtWidgets import QApplication
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
        # Main window background: prefer downloaded landscape, fall back to generated
        bg_path = resource_path("assets/images/frost_bg.png")
        if not os.path.exists(bg_path):
            bg_path = resource_path("assets/images/frost_bg_generated.png")
        if os.path.exists(bg_path):
            palette = self.palette()
            bg_pix = QPixmap(bg_path)
            if not bg_pix.isNull():
                palette.setBrush(QPalette.ColorRole.Window, QBrush(bg_pix))
                self.setPalette(palette)
                self.setAutoFillBackground(True)

        # Parchment texture on journal and quest log editors
        parch_path = resource_path("assets/images/parchment_warm.png")
        if not os.path.exists(parch_path):
            parch_path = resource_path("assets/images/parchment_bg.png")
        if os.path.exists(parch_path):
            parch_pix = QPixmap(parch_path)
            if not parch_pix.isNull():
                for editor in (self.journal.editor, self.quest_log.editor):
                    p = editor.palette()
                    p.setBrush(QPalette.ColorRole.Base, QBrush(parch_pix))
                    editor.setPalette(p)
                    editor.setAutoFillBackground(True)

        # Summary texture (prefer processed over generated)
        summary_path = resource_path("assets/images/summary_bg.png")
        if not os.path.exists(summary_path):
            summary_path = resource_path("assets/images/summary_bg_generated.png")
        if os.path.exists(summary_path):
            summary = self.session_tab.summary_display
            p = summary.palette()
            summary_pix = QPixmap(summary_path)
            if not summary_pix.isNull():
                p.setBrush(QPalette.ColorRole.Base, QBrush(summary_pix))
                summary.setPalette(p)
                summary.setAutoFillBackground(True)

    def _add_decorative_overlays(self):
        """Add gold filigree corner decorations to key panels."""
        self._journal_filigree = GoldFiligreeOverlay(self.journal)
        self._quest_filigree = GoldFiligreeOverlay(self.quest_log)
        self._session_filigree = GoldFiligreeOverlay(self.session_tab)

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
        quill_icon_path = resource_path("assets/images/tab_icon_questlog.png")
        crystal_icon_path = resource_path("assets/images/tab_icon_session.png")

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

        if os.path.exists(crystal_icon_path):
            self.right_tabs.addTab(self.session_tab, QIcon(crystal_icon_path), "Session")
        else:
            self.right_tabs.addTab(self.session_tab, "Session")

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

        name, ok = QInputDialog.getItem(
            self, "Supprimer une campagne",
            "Choisissez la campagne à supprimer:", campaigns, 0, False
        )
        if not ok:
            return

        confirm = QMessageBox.question(
            self, "Confirmer la suppression",
            f"Supprimer la campagne \"{name}\" ?\n"
            "Les fichiers seront déplacés dans campaigns/_trash/.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
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
            QMessageBox.information(self, "Restaurer", "Aucune campagne archivée.")
            return
        trashed = sorted(
            d for d in os.listdir(trash_dir)
            if os.path.isdir(os.path.join(trash_dir, d))
        )
        if not trashed:
            QMessageBox.information(self, "Restaurer", "Aucune campagne archivée.")
            return

        name, ok = QInputDialog.getItem(
            self, "Restaurer une campagne",
            "Choisissez la campagne à restaurer:", trashed, 0, False
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
            lambda msg: QMessageBox.warning(
                self, "Mise à jour",
                f"Impossible de vérifier les mises à jour.\n{msg}",
            )
        )
        self._update_worker.no_update.connect(self._on_update_thread_done)
        self._update_worker.error.connect(self._on_update_thread_done)
        self._update_thread.start()

    def _on_update_available(self, tag, name, url, body):
        self._on_update_thread_done()
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Information)
        box.setWindowTitle("Mise à jour disponible")
        box.setText(f"Version {tag} disponible !\n{name}")
        box.setDetailedText(body)
        btn_download = box.addButton("Télécharger et installer", QMessageBox.ButtonRole.AcceptRole)
        box.addButton("Plus tard", QMessageBox.ButtonRole.RejectRole)
        box.exec()
        if box.clickedButton() == btn_download:
            self._start_update_download(url)

    def _on_no_update(self):
        QMessageBox.information(
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
        confirm = QMessageBox.question(
            self, "Mise à jour",
            "Téléchargement terminé.\n"
            "L'application va se fermer pour installer la mise à jour.\n\n"
            "Continuer ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
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
        QMessageBox.warning(
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
        settings = QSettings("DnDLogger", "DnDLogger")
        geo = settings.value("geometry")
        if geo:
            self.restoreGeometry(geo)
        state = settings.value("windowState")
        if state:
            self.restoreState(state)

    def _save_geometry(self):
        """Save window size/position."""
        settings = QSettings("DnDLogger", "DnDLogger")
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
        from PyQt6.QtCore import QElapsedTimer

        timer = QElapsedTimer()
        timer.start()
        app = QApplication.instance()
        while timer.elapsed() < 500:
            if app:
                app.processEvents()
        event.accept()
