"""Settings dialog and First-Run Wizard."""

import os

from PyQt6.QtCore import QObject, QThread, Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QPalette, QPixmap
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .audio_recorder import AudioRecorder
from .frost_overlay import GoldFiligreeOverlay
from .utils import (
    active_campaign_name,
    campaign_drive_config,
    resource_path,
    save_config,
)


class SettingsDialog(QDialog):
    """Multi-tab settings dialog."""

    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self._config = dict(config)  # Work on a copy
        self.setWindowTitle("Paramètres — DnD Logger")
        self.setMinimumSize(520, 420)
        self._build_ui()
        self._populate()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()

        # === API Tab ===
        api_tab = QWidget()
        api_layout = QFormLayout(api_tab)

        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setPlaceholderText("Entrez votre cle API Mistral...")
        api_layout.addRow("Clé API Mistral:", self.api_key_edit)

        self.btn_test_api = QPushButton("Tester la connexion")
        self.btn_test_api.setObjectName("btn_primary")
        self.btn_test_api.clicked.connect(self._test_api)
        api_layout.addRow("", self.btn_test_api)

        self.api_status = QLabel("")
        api_layout.addRow("", self.api_status)

        self.summary_model_edit = QLineEdit()
        self.summary_model_edit.setPlaceholderText("mistral-large-latest")
        api_layout.addRow("Modèle de résumé:", self.summary_model_edit)

        self.tabs.addTab(api_tab, "API")

        # === Audio Tab ===
        audio_tab = QWidget()
        audio_layout = QFormLayout(audio_tab)

        self.device_combo = QComboBox()
        self._devices = AudioRecorder.list_devices()
        self.device_combo.addItem("Défaut (automatique)", None)
        for dev in self._devices:
            self.device_combo.addItem(dev["name"], dev["index"])
        audio_layout.addRow("Périphérique d'entrée:", self.device_combo)

        self.btn_test_mic = QPushButton("Tester le microphone")
        self.btn_test_mic.clicked.connect(self._test_mic)
        audio_layout.addRow("", self.btn_test_mic)

        self.sample_rate_spin = QSpinBox()
        self.sample_rate_spin.setRange(8000, 48000)
        self.sample_rate_spin.setSingleStep(8000)
        audio_layout.addRow("Fréquence d'échantillonnage:", self.sample_rate_spin)

        self.tabs.addTab(audio_tab, "Audio")

        # === Advanced Tab ===
        adv_tab = QWidget()
        adv_layout = QFormLayout(adv_tab)

        self.auto_update_check = QCheckBox("Vérifier les mises à jour au démarrage")
        adv_layout.addRow(self.auto_update_check)

        self.chunk_spin = QSpinBox()
        self.chunk_spin.setRange(10, 300)
        self.chunk_spin.setSuffix(" min")
        adv_layout.addRow("Durée max par chunk:", self.chunk_spin)

        self.bias_edit = QTextEdit()
        self.bias_edit.setMaximumHeight(120)
        self.bias_edit.setPlaceholderText("Termes D&D (un par ligne)...")
        adv_layout.addRow("Biais de contexte D&D:", self.bias_edit)

        self.tabs.addTab(adv_tab, "Avancé")

        # === Google Drive Tab ===
        drive_tab = QWidget()
        drive_layout = QVBoxLayout(drive_tab)

        # Account group
        account_group = QGroupBox("Compte Google")
        account_form = QFormLayout(account_group)

        self.drive_status_label = QLabel("Non connecté")
        self.drive_status_label.setStyleSheet("color: #8899aa;")
        account_form.addRow("Statut:", self.drive_status_label)

        btn_row = QHBoxLayout()
        self.btn_drive_login = QPushButton("Se connecter")
        self.btn_drive_login.setObjectName("btn_primary")
        self.btn_drive_login.clicked.connect(self._drive_login)
        self.btn_drive_logout = QPushButton("Se déconnecter")
        self.btn_drive_logout.clicked.connect(self._drive_logout)
        self.btn_drive_logout.setEnabled(False)
        btn_row.addWidget(self.btn_drive_login)
        btn_row.addWidget(self.btn_drive_logout)
        btn_row.addStretch()
        account_form.addRow("", btn_row)

        drive_layout.addWidget(account_group)

        # Campaign sync group
        campaign_group = QGroupBox("Synchronisation de campagne")
        campaign_form = QFormLayout(campaign_group)

        campaign_label = QLabel("")
        campaign_label.setStyleSheet("color: #d4af37;")
        self._drive_campaign_label = campaign_label
        campaign_form.addRow("Campagne active:", campaign_label)

        join_row = QHBoxLayout()
        self.drive_join_id = QLineEdit()
        self.drive_join_id.setPlaceholderText("Coller l'ID du dossier partagé...")
        join_row.addWidget(self.drive_join_id)
        join_row.addWidget(QLabel("(pour rejoindre)"))
        campaign_form.addRow("Rejoindre:", join_row)

        folder_row = QHBoxLayout()
        self.drive_folder_id_label = QLineEdit()
        self.drive_folder_id_label.setReadOnly(True)
        self.drive_folder_id_label.setPlaceholderText("Aucun dossier créé")
        self.btn_copy_folder_id = QPushButton("Copier")
        self.btn_copy_folder_id.setFixedWidth(100)
        self.btn_copy_folder_id.clicked.connect(self._copy_folder_id)
        folder_row.addWidget(self.drive_folder_id_label)
        folder_row.addWidget(self.btn_copy_folder_id)
        campaign_form.addRow("ID du dossier:", folder_row)

        drive_layout.addWidget(campaign_group)

        # Sync toggle
        self.drive_sync_checkbox = QCheckBox("Activer la synchronisation Google Drive")
        self.drive_sync_checkbox.toggled.connect(self._on_sync_toggled)
        drive_layout.addWidget(self.drive_sync_checkbox)

        drive_layout.addStretch()
        self.tabs.addTab(drive_tab, "Google Drive")

        self._auth_thread = None
        self._auth_worker = None
        self._folder_thread = None
        self._folder_worker = None

        layout.addWidget(self.tabs)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self._save_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _populate(self):
        """Fill fields from config."""
        self.api_key_edit.setText(self._config.get("api_key", ""))
        self.summary_model_edit.setText(self._config.get("summary_model", "mistral-large-latest"))

        # Device
        dev = self._config.get("audio_device")
        if dev is not None:
            idx = self.device_combo.findData(dev)
            if idx >= 0:
                self.device_combo.setCurrentIndex(idx)

        self.sample_rate_spin.setValue(self._config.get("sample_rate", 16000))
        self.auto_update_check.setChecked(self._config.get("auto_update_check", True))
        self.chunk_spin.setValue(self._config.get("chunk_duration_minutes", 150))

        bias = self._config.get("context_bias", [])
        self.bias_edit.setPlainText("\n".join(bias))

        # Drive tab — read from campaign config
        cname = active_campaign_name(self._config)
        self._drive_campaign_label.setText(cname)
        drive_cfg = campaign_drive_config(self._config)
        folder_id = drive_cfg.get("drive_campaign_folder_id", "")
        self.drive_folder_id_label.setText(folder_id)
        self.drive_sync_checkbox.setChecked(drive_cfg.get("drive_sync_enabled", False))

        # Check existing credentials
        self._refresh_drive_status()

    def _save_and_accept(self):
        """Save settings to config and close."""
        self._config["api_key"] = self.api_key_edit.text().strip()
        self._config["summary_model"] = self.summary_model_edit.text().strip() or "mistral-large-latest"
        self._config["audio_device"] = self.device_combo.currentData()
        self._config["sample_rate"] = self.sample_rate_spin.value()
        self._config["chunk_duration_minutes"] = self.chunk_spin.value()
        self._config["auto_update_check"] = self.auto_update_check.isChecked()

        bias_text = self.bias_edit.toPlainText().strip()
        self._config["context_bias"] = [line.strip() for line in bias_text.split("\n") if line.strip()]

        # Drive settings — write into campaigns dict
        cname = active_campaign_name(self._config)
        if "campaigns" not in self._config:
            self._config["campaigns"] = {}
        if cname not in self._config["campaigns"]:
            self._config["campaigns"][cname] = {}

        join_id = self.drive_join_id.text().strip()
        if join_id:
            self._config["campaigns"][cname]["drive_campaign_folder_id"] = join_id
        self._config["campaigns"][cname]["drive_sync_enabled"] = self.drive_sync_checkbox.isChecked()

        save_config(self._config)
        self.accept()

    def get_config(self) -> dict:
        return self._config

    # ── Google Drive ────────────────────────────────────────

    def _refresh_drive_status(self):
        """Update the Drive account status label from saved credentials."""
        try:
            from .drive_auth import get_user_email, load_credentials

            creds = load_credentials()
            if creds and creds.valid:
                email = get_user_email(creds)
                self.drive_status_label.setText(email or "Connecté")
                self.drive_status_label.setStyleSheet("color: #7ec83a;")
                self.btn_drive_login.setEnabled(False)
                self.btn_drive_logout.setEnabled(True)
            else:
                self.drive_status_label.setText("Non connecté")
                self.drive_status_label.setStyleSheet("color: #8899aa;")
                self.btn_drive_login.setEnabled(True)
                self.btn_drive_logout.setEnabled(False)
        except ImportError:
            self.drive_status_label.setText("Dépendances Google manquantes")
            self.drive_status_label.setStyleSheet("color: #ff6b6b;")
            self.btn_drive_login.setEnabled(False)

    def _drive_login(self):
        """Start the OAuth2 login flow."""
        try:
            from .drive_auth import start_auth_flow

            self.btn_drive_login.setEnabled(False)
            self.btn_drive_login.setText("Connexion en cours...")
            self._auth_thread, self._auth_worker = start_auth_flow()
            self._auth_worker.auth_completed.connect(self._on_auth_completed)
            self._auth_worker.auth_failed.connect(self._on_auth_failed)
            self._auth_thread.start()
        except ImportError:
            QMessageBox.critical(
                self,
                "Erreur",
                "Installez les dépendances Google:\n"
                "pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib",
            )

    def _on_auth_completed(self, creds):
        """OAuth2 flow completed successfully."""
        self.btn_drive_login.setText("Se connecter")
        self._refresh_drive_status()

    def _on_auth_failed(self, error: str):
        """OAuth2 flow failed."""
        self.btn_drive_login.setText("Se connecter")
        self.btn_drive_login.setEnabled(True)
        QMessageBox.warning(self, "Échec de connexion", f"Erreur: {error}")

    def _drive_logout(self):
        """Disconnect from Google Drive."""
        from .drive_auth import delete_credentials

        delete_credentials()
        self._refresh_drive_status()

    def _on_sync_toggled(self, checked: bool):
        """When sync is ticked on, resolve the Drive folder ID immediately."""
        if not checked:
            return
        # Already have a folder ID (from join field or previous run)?
        if self.drive_folder_id_label.text():
            return

        cname = active_campaign_name(self._config)
        self.drive_folder_id_label.setPlaceholderText("Création du dossier...")

        self._folder_worker = _FolderWorker(cname)
        self._folder_thread = QThread()
        self._folder_worker.moveToThread(self._folder_thread)
        self._folder_thread.started.connect(self._folder_worker.run)
        self._folder_worker.finished.connect(self._on_folder_resolved)
        self._folder_worker.error.connect(self._on_folder_error)
        self._folder_thread.start()

    def _on_folder_resolved(self, folder_id: str):
        """Drive folder was created / found — show the ID."""
        if self._folder_thread:
            self._folder_thread.quit()
            self._folder_thread.wait()
            self._folder_thread = None
            self._folder_worker = None
        self.drive_folder_id_label.setText(folder_id)
        self.drive_folder_id_label.setPlaceholderText("Aucun dossier créé")
        # Also store it so _save_and_accept persists it
        cname = active_campaign_name(self._config)
        if "campaigns" not in self._config:
            self._config["campaigns"] = {}
        if cname not in self._config["campaigns"]:
            self._config["campaigns"][cname] = {}
        self._config["campaigns"][cname]["drive_campaign_folder_id"] = folder_id

    def _on_folder_error(self, error: str):
        """Drive folder resolution failed."""
        if self._folder_thread:
            self._folder_thread.quit()
            self._folder_thread.wait()
            self._folder_thread = None
            self._folder_worker = None
        self.drive_folder_id_label.setPlaceholderText("Aucun dossier créé")
        QMessageBox.warning(self, "Google Drive", f"Impossible de créer le dossier: {error}")

    def _copy_folder_id(self):
        """Copy the campaign folder ID to clipboard."""
        folder_id = self.drive_folder_id_label.text()
        if folder_id:
            from PyQt6.QtWidgets import QApplication

            QApplication.clipboard().setText(folder_id)

    def _test_api(self):
        """Test the Mistral API connection."""
        key = self.api_key_edit.text().strip()
        if not key:
            self.api_status.setText("Entrez une clé API d'abord.")
            self.api_status.setStyleSheet("color: #ff6b6b;")
            return
        try:
            from mistralai import Mistral

            client = Mistral(api_key=key)
            result = client.models.list()
            self.api_status.setText("Connexion réussie !")
            self.api_status.setStyleSheet("color: #7ec83a;")
        except Exception as e:
            self.api_status.setText(f"Échec: {e}")
            self.api_status.setStyleSheet("color: #ff6b6b;")

    def _test_mic(self):
        """Quick microphone test."""
        try:
            import numpy as np
            import sounddevice as sd

            dev = self.device_combo.currentData()
            sr = self.sample_rate_spin.value()
            data = sd.rec(int(sr * 1), samplerate=sr, channels=1, dtype="int16", device=dev)
            sd.wait()
            rms = np.sqrt(np.mean(data.astype(np.float32) ** 2))
            if rms > 100:
                QMessageBox.information(self, "Test Microphone", f"Microphone fonctionne ! (niveau: {rms:.0f})")
            else:
                QMessageBox.warning(self, "Test Microphone", "Signal très faible. Vérifiez votre microphone.")
        except Exception as e:
            QMessageBox.critical(self, "Test Microphone", f"Erreur: {e}")



class _FolderWorker(QObject):
    """Resolve the Drive campaign folder ID in a background thread."""
    finished = pyqtSignal(str)   # folder_id
    error = pyqtSignal(str)

    def __init__(self, campaign_name: str):
        super().__init__()
        self._campaign_name = campaign_name

    def run(self):
        try:
            from .drive_auth import load_credentials
            from .drive_sync import DriveFolderManager
            from googleapiclient.discovery import build

            creds = load_credentials()
            if not creds:
                self.error.emit("Non connecté à Google Drive")
                return
            service = build("drive", "v3", credentials=creds)
            mgr = DriveFolderManager(service)
            folder_id = mgr.get_or_create_campaign_folder(self._campaign_name)
            self.finished.emit(folder_id)
        except Exception as e:
            self.error.emit(str(e))


class FirstRunWizard(QDialog):
    """Shown on first launch when no API key is configured."""

    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self._config = config
        self.setWindowTitle("Bienvenue — DnD Logger")
        self.setMinimumSize(520, 440)
        self._build_ui()
        self._apply_theme()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Banner
        banner_path = resource_path("assets/images/banner_dndlogger.png")
        if os.path.exists(banner_path):
            banner_pix = QPixmap(banner_path)
            if not banner_pix.isNull():
                banner_label = QLabel()
                banner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                banner_label.setPixmap(banner_pix.scaledToWidth(480, Qt.TransformationMode.SmoothTransformation))
                layout.addWidget(banner_label)
                layout.addSpacing(8)
        else:
            # Fallback text title
            title = QLabel("Bienvenue dans DnD Logger")
            title.setObjectName("heading")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title)

        subtitle = QLabel("Votre compagnon de session D&D.\n" "Configurons les éléments essentiels pour commencer.")
        subtitle.setObjectName("subheading")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        # API Key
        api_group = QGroupBox("Clé API Mistral")
        api_layout = QFormLayout(api_group)
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setPlaceholderText("Entrez votre clé API Mistral...")
        api_layout.addRow(self.api_key_edit)

        api_hint = QLabel("Obtenez une clé sur console.mistral.ai")
        api_hint.setStyleSheet("color: #8899aa; font-size: 11px;")
        api_layout.addRow(api_hint)
        layout.addWidget(api_group)

        # Audio
        audio_group = QGroupBox("Microphone")
        audio_layout = QFormLayout(audio_group)
        self.device_combo = QComboBox()
        self._devices = AudioRecorder.list_devices()
        self.device_combo.addItem("Défaut (automatique)", None)
        for dev in self._devices:
            self.device_combo.addItem(dev["name"], dev["index"])
        audio_layout.addRow("Périphérique:", self.device_combo)
        layout.addWidget(audio_group)

        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_skip = QPushButton("Configurer plus tard")
        self.btn_done = QPushButton("Commencer l'aventure !")
        self.btn_done.setObjectName("btn_gold")
        btn_layout.addWidget(self.btn_skip)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_done)
        layout.addLayout(btn_layout)

        self.btn_skip.clicked.connect(self.reject)
        self.btn_done.clicked.connect(self._finish)

    def _apply_theme(self):
        """Apply frost-themed background and overlays to the wizard."""
        # Dimmed frost background
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

        # Frost corner decorations
        self._filigree_overlay = GoldFiligreeOverlay(self)

    def _finish(self):
        key = self.api_key_edit.text().strip()
        if key:
            self._config["api_key"] = key
        dev = self.device_combo.currentData()
        self._config["audio_device"] = dev

        save_config(self._config)
        self.accept()

    def get_config(self) -> dict:
        return self._config
