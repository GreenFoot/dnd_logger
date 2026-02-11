"""Settings dialog and First-Run Wizard."""

import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QPalette, QPixmap
from PyQt6.QtWidgets import (
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
from .utils import resource_path, save_config


class SettingsDialog(QDialog):
    """Multi-tab settings dialog."""

    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self._config = dict(config)  # Work on a copy
        self.setWindowTitle("Paramètres — Icewind Dale")
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
        self.summary_model_edit.setPlaceholderText("mistral-small-latest")
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

        self.chunk_spin = QSpinBox()
        self.chunk_spin.setRange(10, 300)
        self.chunk_spin.setSuffix(" min")
        adv_layout.addRow("Durée max par chunk:", self.chunk_spin)

        self.bias_edit = QTextEdit()
        self.bias_edit.setMaximumHeight(120)
        self.bias_edit.setPlaceholderText("Termes D&D (un par ligne)...")
        adv_layout.addRow("Biais de contexte D&D:", self.bias_edit)

        self.tabs.addTab(adv_tab, "Avancé")

        layout.addWidget(self.tabs)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self._save_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _populate(self):
        """Fill fields from config."""
        self.api_key_edit.setText(self._config.get("api_key", ""))
        self.summary_model_edit.setText(self._config.get("summary_model", "mistral-small-latest"))

        # Device
        dev = self._config.get("audio_device")
        if dev is not None:
            idx = self.device_combo.findData(dev)
            if idx >= 0:
                self.device_combo.setCurrentIndex(idx)

        self.sample_rate_spin.setValue(self._config.get("sample_rate", 16000))
        self.chunk_spin.setValue(self._config.get("chunk_duration_minutes", 150))

        bias = self._config.get("context_bias", [])
        self.bias_edit.setPlainText("\n".join(bias))

    def _save_and_accept(self):
        """Save settings to config and close."""
        self._config["api_key"] = self.api_key_edit.text().strip()
        self._config["summary_model"] = self.summary_model_edit.text().strip() or "mistral-small-latest"
        self._config["audio_device"] = self.device_combo.currentData()
        self._config["sample_rate"] = self.sample_rate_spin.value()
        self._config["chunk_duration_minutes"] = self.chunk_spin.value()

        bias_text = self.bias_edit.toPlainText().strip()
        self._config["context_bias"] = [line.strip() for line in bias_text.split("\n") if line.strip()]

        save_config(self._config)
        self.accept()

    def get_config(self) -> dict:
        return self._config

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


class FirstRunWizard(QDialog):
    """Shown on first launch when no API key is configured."""

    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self._config = config
        self.setWindowTitle("Bienvenue — Icewind Dale")
        self.setMinimumSize(520, 440)
        self._build_ui()
        self._apply_theme()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Banner
        banner_path = resource_path("assets/images/banner_icewind.png")
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
            title = QLabel("Bienvenue dans Icewind Dale")
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
