"""Settings dialog and First-Run Wizard."""

import os

from PySide6.QtCore import QObject, Qt, QThread, Signal
from PySide6.QtGui import QBrush, QPalette, QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from . import themed_dialogs as dlg
from .audio_recorder import AudioRecorder
from .filigree_overlay import GoldFiligreeOverlay
from .i18n import set_language, tr
from .quest_extractor import get_default_quest_extraction
from .summarizer import get_default_condense, get_default_summary_system
from .utils import active_campaign_name, campaign_drive_config, resource_path, save_config


class SettingsDialog(QDialog):
    """Multi-tab settings dialog."""

    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self._config = dict(config)  # Work on a copy
        self._initial_language = config.get("language", "en")
        self._current_prompt_index = 0
        self._auth_thread = None
        self._auth_worker = None
        self._folder_thread = None
        self._folder_worker = None
        self.setWindowTitle(tr("settings.title"))
        self._build_ui()
        self._populate()
        self.tabs.setStyleSheet("QTabBar::tab { padding: 8px 14px; }")
        self.adjustSize()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()

        # === API Tab ===
        api_tab = QWidget()
        api_layout = QFormLayout(api_tab)

        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setPlaceholderText(tr("settings.api.key_placeholder"))
        api_layout.addRow(tr("settings.api.key_label"), self.api_key_edit)

        self.btn_test_api = QPushButton(tr("settings.api.btn_test"))
        self.btn_test_api.setObjectName("btn_primary")
        self.btn_test_api.clicked.connect(self._test_api)
        api_layout.addRow("", self.btn_test_api)

        self.api_status = QLabel("")
        api_layout.addRow("", self.api_status)

        self.summary_model_edit = QLineEdit()
        self.summary_model_edit.setPlaceholderText("mistral-large-latest")
        api_layout.addRow(tr("settings.api.model_label"), self.summary_model_edit)

        self.tabs.addTab(api_tab, tr("settings.tab.api"))

        # === Audio Tab ===
        audio_tab = QWidget()
        audio_layout = QFormLayout(audio_tab)

        self.device_combo = QComboBox()
        self._devices = AudioRecorder.list_devices()
        self.device_combo.addItem(tr("settings.audio.device_default"), None)
        for dev in self._devices:
            self.device_combo.addItem(dev["name"], dev["index"])
        audio_layout.addRow(tr("settings.audio.device_label"), self.device_combo)

        self.btn_test_mic = QPushButton(tr("settings.audio.btn_test_mic"))
        self.btn_test_mic.clicked.connect(self._test_mic)
        audio_layout.addRow("", self.btn_test_mic)

        self.sample_rate_spin = QSpinBox()
        self.sample_rate_spin.setRange(8000, 48000)
        self.sample_rate_spin.setSingleStep(8000)
        audio_layout.addRow(tr("settings.audio.sample_rate_label"), self.sample_rate_spin)

        self.tabs.addTab(audio_tab, tr("settings.tab.audio"))

        # === Advanced Tab ===
        adv_tab = QWidget()
        adv_layout = QFormLayout(adv_tab)

        self.auto_update_check = QCheckBox(tr("settings.advanced.auto_update"))
        adv_layout.addRow(self.auto_update_check)

        self.chunk_spin = QSpinBox()
        self.chunk_spin.setRange(10, 300)
        self.chunk_spin.setSuffix(" min")
        adv_layout.addRow(tr("settings.advanced.chunk_label"), self.chunk_spin)

        self.bias_edit = QTextEdit()
        self.bias_edit.setMaximumHeight(120)
        self.bias_edit.setPlaceholderText(tr("settings.advanced.bias_placeholder"))
        adv_layout.addRow(tr("settings.advanced.bias_label"), self.bias_edit)

        # Language selector
        self.language_combo = QComboBox()
        self.language_combo.addItem("English", "en")
        self.language_combo.addItem("Français", "fr")
        self.language_combo.addItem("Deutsch", "de")
        self.language_combo.addItem("Español", "es")
        self.language_combo.addItem("Italiano", "it")
        self.language_combo.addItem("Nederlands", "nl")
        self.language_combo.addItem("Português", "pt")
        adv_layout.addRow(tr("settings.advanced.language_label"), self.language_combo)

        self.tabs.addTab(adv_tab, tr("settings.tab.advanced"))

        # === Prompts Tab ===
        prompts_tab = QWidget()
        prompts_layout = QVBoxLayout(prompts_tab)

        # Prompt selector
        selector_row = QHBoxLayout()
        selector_row.addWidget(QLabel(tr("settings.prompts.prompt_label")))
        self.prompt_combo = QComboBox()
        self._prompt_keys = [
            ("prompt_summary_system", tr("settings.prompts.summary_system_label"), get_default_summary_system),
            ("prompt_condense", tr("settings.prompts.condense_label"), get_default_condense),
            ("prompt_quest_extraction", tr("settings.prompts.quest_extraction_label"), get_default_quest_extraction),
        ]
        for _key, label, _default_fn in self._prompt_keys:
            self.prompt_combo.addItem(label)
        self.prompt_combo.currentIndexChanged.connect(self._on_prompt_selected)
        selector_row.addWidget(self.prompt_combo, stretch=1)
        prompts_layout.addLayout(selector_row)

        # Placeholder info
        self.prompt_info_label = QLabel("")
        self.prompt_info_label.setStyleSheet("color: #8899aa; font-size: 11px;")
        self.prompt_info_label.setWordWrap(True)
        prompts_layout.addWidget(self.prompt_info_label)

        # Prompt editor
        self.prompt_edit = QTextEdit()
        self.prompt_edit.setAcceptRichText(False)
        self.prompt_edit.textChanged.connect(self._on_prompt_text_changed)
        prompts_layout.addWidget(self.prompt_edit, stretch=1)

        # Reset button
        btn_row_prompts = QHBoxLayout()
        btn_row_prompts.addStretch()
        self.btn_reset_prompt = QPushButton(tr("settings.prompts.btn_reset"))
        self.btn_reset_prompt.clicked.connect(self._reset_current_prompt)
        btn_row_prompts.addWidget(self.btn_reset_prompt)
        prompts_layout.addLayout(btn_row_prompts)

        # Internal storage for edited prompts
        self._prompt_texts = {}
        self.tabs.addTab(prompts_tab, tr("settings.tab.prompts"))

        # === Google Drive Tab ===
        drive_tab = QWidget()
        drive_layout = QVBoxLayout(drive_tab)

        # Account group
        account_group = QGroupBox(tr("settings.drive.account_group"))
        account_form = QFormLayout(account_group)

        self.drive_status_label = QLabel(tr("settings.drive.not_connected"))
        self.drive_status_label.setStyleSheet("color: #8899aa;")
        account_form.addRow(tr("settings.drive.status_label"), self.drive_status_label)

        btn_row = QHBoxLayout()
        self.btn_drive_login = QPushButton(tr("settings.drive.btn_login"))
        self.btn_drive_login.setObjectName("btn_primary")
        self.btn_drive_login.clicked.connect(self._drive_login)
        self.btn_drive_logout = QPushButton(tr("settings.drive.btn_logout"))
        self.btn_drive_logout.clicked.connect(self._drive_logout)
        self.btn_drive_logout.setEnabled(False)
        btn_row.addWidget(self.btn_drive_login)
        btn_row.addWidget(self.btn_drive_logout)
        btn_row.addStretch()
        account_form.addRow("", btn_row)

        drive_layout.addWidget(account_group)

        # Campaign sync group
        campaign_group = QGroupBox(tr("settings.drive.campaign_sync_group"))
        campaign_form = QFormLayout(campaign_group)

        campaign_label = QLabel("")
        campaign_label.setStyleSheet("color: #d4af37;")
        self._drive_campaign_label = campaign_label
        campaign_form.addRow(tr("settings.drive.active_campaign_label"), campaign_label)

        join_row = QHBoxLayout()
        self.drive_join_id = QLineEdit()
        self.drive_join_id.setPlaceholderText(tr("settings.drive.join_placeholder"))
        join_row.addWidget(self.drive_join_id)
        join_row.addWidget(QLabel(tr("settings.drive.join_hint")))
        campaign_form.addRow(tr("settings.drive.folder_id_label"), join_row)

        folder_row = QHBoxLayout()
        self.drive_folder_id_label = QLineEdit()
        self.drive_folder_id_label.setReadOnly(True)
        self.drive_folder_id_label.setPlaceholderText(tr("settings.drive.no_folder"))
        self.btn_copy_folder_id = QPushButton(tr("settings.drive.btn_copy"))
        self.btn_copy_folder_id.setFixedWidth(100)
        self.btn_copy_folder_id.clicked.connect(self._copy_folder_id)
        folder_row.addWidget(self.drive_folder_id_label)
        folder_row.addWidget(self.btn_copy_folder_id)
        campaign_form.addRow(tr("settings.drive.folder_id_label"), folder_row)

        drive_layout.addWidget(campaign_group)

        # Sync toggle
        self.drive_sync_checkbox = QCheckBox(tr("settings.drive.sync_checkbox"))
        self.drive_sync_checkbox.toggled.connect(self._on_sync_toggled)
        drive_layout.addWidget(self.drive_sync_checkbox)

        drive_layout.addStretch()
        self.tabs.addTab(drive_tab, tr("settings.tab.drive"))

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

        # Language
        lang = self._config.get("language", "en")
        lang_idx = self.language_combo.findData(lang)
        if lang_idx >= 0:
            self.language_combo.setCurrentIndex(lang_idx)

        # Prompts — load custom or show default
        for key, _label, _default_fn in self._prompt_keys:
            custom = self._config.get(key, "")
            self._prompt_texts[key] = custom
        self._on_prompt_selected(0)

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

        # Language
        new_lang = self.language_combo.currentData()
        self._config["language"] = new_lang

        # Prompts — save current editor state, then store all
        self._store_current_prompt()
        for key, _label, _default_fn in self._prompt_keys:
            self._config[key] = self._prompt_texts.get(key, "")

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

        # Apply language change immediately (no restart needed)
        if new_lang != self._initial_language:
            set_language(new_lang)

        self.accept()

    def get_config(self) -> dict:
        """Return the current configuration dictionary."""
        return self._config

    # ── Prompts ────────────────────────────────────────────

    _PLACEHOLDER_HINTS = {
        "prompt_summary_system": "settings.prompts.hint.summary_system",
        "prompt_condense": "settings.prompts.hint.condense",
        "prompt_quest_extraction": "settings.prompts.hint.quest_extraction",
    }

    def _on_prompt_selected(self, index: int):
        """Switch the editor to the selected prompt."""
        # Save text of previously selected prompt
        self._store_current_prompt()
        self._current_prompt_index = index
        key, _label, default_fn = self._prompt_keys[index]
        custom = self._prompt_texts.get(key, "")
        self.prompt_edit.setPlainText(custom if custom else default_fn())
        hint_key = self._PLACEHOLDER_HINTS.get(key, "")
        self.prompt_info_label.setText(tr(hint_key) if hint_key else "")
        self.btn_reset_prompt.setEnabled(bool(custom))

    def _on_prompt_text_changed(self):
        """Enable the reset button when the editor text differs from default."""
        if not hasattr(self, "_current_prompt_index"):
            return
        _key, _label, default_fn = self._prompt_keys[self._current_prompt_index]
        text = self.prompt_edit.toPlainText().strip()
        self.btn_reset_prompt.setEnabled(text != default_fn().strip())

    def _store_current_prompt(self):
        """Save the editor text back to the internal dict."""
        if not hasattr(self, "_current_prompt_index"):
            return
        key, _label, default_fn = self._prompt_keys[self._current_prompt_index]
        text = self.prompt_edit.toPlainText().strip()
        # Store empty string if text matches default (= no customization)
        if text == default_fn().strip():
            self._prompt_texts[key] = ""
        else:
            self._prompt_texts[key] = text
        self.btn_reset_prompt.setEnabled(bool(self._prompt_texts[key]))

    def _reset_current_prompt(self):
        """Reset the current prompt to its built-in default."""
        key, _label, default_fn = self._prompt_keys[self._current_prompt_index]
        self.prompt_edit.setPlainText(default_fn())
        self._prompt_texts[key] = ""
        self.btn_reset_prompt.setEnabled(False)

    # ── Google Drive ────────────────────────────────────────

    def _refresh_drive_status(self):
        """Update the Drive account status label from saved credentials."""
        try:
            from .drive_auth import get_user_email, load_credentials

            creds = load_credentials()
            if creds and creds.valid:
                email = get_user_email(creds)
                self.drive_status_label.setText(email or tr("settings.drive.connected"))
                self.drive_status_label.setStyleSheet("color: #7ec83a;")
                self.btn_drive_login.setEnabled(False)
                self.btn_drive_logout.setEnabled(True)
            else:
                self.drive_status_label.setText(tr("settings.drive.not_connected"))
                self.drive_status_label.setStyleSheet("color: #8899aa;")
                self.btn_drive_login.setEnabled(True)
                self.btn_drive_logout.setEnabled(False)
        except ImportError:
            self.drive_status_label.setText(tr("settings.drive.deps_missing"))
            self.drive_status_label.setStyleSheet("color: #ff6b6b;")
            self.btn_drive_login.setEnabled(False)

    def _drive_login(self):
        """Start the OAuth2 login flow."""
        try:
            from .drive_auth import start_auth_flow

            self.btn_drive_login.setEnabled(False)
            self.btn_drive_login.setText(tr("settings.drive.logging_in"))
            self._auth_thread, self._auth_worker = start_auth_flow()
            self._auth_worker.auth_completed.connect(self._on_auth_completed)
            self._auth_worker.auth_failed.connect(self._on_auth_failed)
            self._auth_thread.start()
        except ImportError:
            dlg.critical(
                self,
                tr("app.campaign.error_title"),
                tr("app.campaign.drive_install_deps"),
            )

    def _on_auth_completed(self, creds):
        """OAuth2 flow completed successfully."""
        self.btn_drive_login.setText(tr("settings.drive.btn_login"))
        self._refresh_drive_status()

    def _on_auth_failed(self, error: str):
        """OAuth2 flow failed."""
        self.btn_drive_login.setText(tr("settings.drive.btn_login"))
        self.btn_drive_login.setEnabled(True)
        dlg.warning(self, tr("settings.drive.login_failed_title"), tr("settings.drive.login_failed", error=error))

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
        self.drive_folder_id_label.setPlaceholderText(tr("settings.drive.creating_folder"))

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
        self.drive_folder_id_label.setPlaceholderText(tr("settings.drive.no_folder"))
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
        self.drive_folder_id_label.setPlaceholderText(tr("settings.drive.no_folder"))
        dlg.warning(self, "Google Drive", tr("settings.drive.folder_error", error=error))

    def _copy_folder_id(self):
        """Copy the campaign folder ID to clipboard."""
        folder_id = self.drive_folder_id_label.text()
        if folder_id:
            from PySide6.QtWidgets import QApplication

            QApplication.clipboard().setText(folder_id)

    def _test_api(self):
        """Test the Mistral API connection."""
        key = self.api_key_edit.text().strip()
        if not key:
            self.api_status.setText(tr("settings.api.enter_key_first"))
            self.api_status.setStyleSheet("color: #ff6b6b;")
            return
        try:
            from mistralai import Mistral

            client = Mistral(api_key=key)
            client.models.list()
            self.api_status.setText(tr("settings.api.test_success"))
            self.api_status.setStyleSheet("color: #7ec83a;")
        except Exception as e:
            self.api_status.setText(tr("settings.api.test_fail", error=e))
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
                dlg.information(self, tr("settings.audio.test_title"), tr("settings.audio.test_ok", level=f"{rms:.0f}"))
            else:
                dlg.warning(self, tr("settings.audio.test_title"), tr("settings.audio.test_weak"))
        except Exception as e:
            dlg.critical(self, tr("settings.audio.test_title"), tr("settings.audio.test_error", error=e))


class _FolderWorker(QObject):
    """Resolve the Drive campaign folder ID in a background thread."""

    finished = Signal(str)  # folder_id
    error = Signal(str)

    def __init__(self, campaign_name: str):
        super().__init__()
        self._campaign_name = campaign_name

    def run(self):
        """Resolve or create the Drive campaign folder."""
        try:
            from googleapiclient.discovery import build

            from .drive_auth import load_credentials
            from .drive_sync import DriveFolderManager

            creds = load_credentials()
            if not creds:
                self.error.emit(tr("settings.drive.not_connected_error"))
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
        self.setWindowTitle(tr("wizard.title"))
        self.setMinimumSize(520, 440)
        self._build_ui()
        self._apply_theme()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Banner
        banner_path = resource_path("assets/images/app/banner_dndlogger.png")
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
            title = QLabel(tr("wizard.welcome"))
            title.setObjectName("heading")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title)

        subtitle = QLabel(tr("wizard.subtitle"))
        subtitle.setObjectName("subheading")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)
        layout.addSpacing(16)

        # API Key
        api_group = QGroupBox(tr("wizard.api_group"))
        api_layout = QFormLayout(api_group)
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setPlaceholderText(tr("wizard.api_placeholder"))
        api_layout.addRow(self.api_key_edit)

        api_hint = QLabel(tr("wizard.api_hint"))
        api_hint.setStyleSheet("color: #8899aa; font-size: 11px;")
        api_layout.addRow(api_hint)
        layout.addWidget(api_group)

        # Audio
        audio_group = QGroupBox(tr("wizard.mic_group"))
        audio_layout = QFormLayout(audio_group)
        self.device_combo = QComboBox()
        self._devices = AudioRecorder.list_devices()
        self.device_combo.addItem(tr("settings.audio.device_default"), None)
        for dev in self._devices:
            self.device_combo.addItem(dev["name"], dev["index"])
        audio_layout.addRow(tr("wizard.mic_device_label"), self.device_combo)
        layout.addWidget(audio_group)

        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_skip = QPushButton(tr("wizard.btn_skip"))
        self.btn_done = QPushButton(tr("wizard.btn_done"))
        self.btn_done.setObjectName("btn_gold")
        btn_layout.addWidget(self.btn_skip)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_done)
        layout.addLayout(btn_layout)

        self.btn_skip.clicked.connect(self.reject)
        self.btn_done.clicked.connect(self._finish)

    def _apply_theme(self):
        """Apply frost-themed background and overlays to the wizard."""
        # Background
        bg_path = resource_path("assets/images/backgrounds/bg_icewind_dale.png")
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
        """Return the current configuration dictionary."""
        return self._config
