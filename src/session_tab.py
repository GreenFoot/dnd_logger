"""Session Tab — recording controls, transcript, and summary display."""

import glob
import os
import shutil
import time
from datetime import datetime

import soundfile as sf

from PyQt6.QtCore import Qt, QRectF, QTimer
from PyQt6.QtGui import QAction, QColor, QPainter
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMenu,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from .audio_recorder import AudioRecorder
from .quest_extractor import QuestProposalDialog, start_quest_extraction
from .snow_particles import AuroraShimmerOverlay, SnowParticleOverlay
from .summarizer import SummarizerWorker, start_summarization
from .transcriber import TranscriptionWorker, start_live_transcription, start_transcription
from .utils import ensure_dir, format_duration, format_file_size, sessions_dir


class _ThinDivider(QWidget):
    """A thin gold divider line with a small center diamond. Height: 12px."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(12)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

    def paintEvent(self, event):
        from PyQt6.QtGui import QColor, QPainter, QPainterPath, QPen

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        cy = self.height() / 2
        margin = 40

        # Thin gold line
        gold = QColor(201, 168, 50, 70)
        painter.setPen(QPen(gold, 1.0))
        painter.drawLine(int(margin), int(cy), int(w - margin), int(cy))

        # Center diamond
        diamond = QPainterPath()
        ds = 4
        diamond.moveTo(w / 2, cy - ds)
        diamond.lineTo(w / 2 + ds, cy)
        diamond.lineTo(w / 2, cy + ds)
        diamond.lineTo(w / 2 - ds, cy)
        diamond.closeSubpath()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(201, 168, 50, 100))
        painter.drawPath(diamond)

        painter.end()


def _make_divider() -> QWidget:
    """Create a thin gold divider widget."""
    return _ThinDivider()


class PostRecordingDialog(QDialog):
    """Dialog shown after stopping recording with options."""

    TRANSCRIBE = "transcribe"
    RE_RECORD = "re_record"
    SAVE_ONLY = "save_only"

    def __init__(self, wav_path: str, duration: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enregistrement terminé")
        self.setMinimumWidth(400)
        self.result_action = self.SAVE_ONLY

        layout = QVBoxLayout(self)

        # Info
        size = os.path.getsize(wav_path) if os.path.exists(wav_path) else 0
        info = QLabel(
            f"Durée: {format_duration(duration)}\n"
            f"Taille: {format_file_size(size)}\n"
            f"Fichier: {os.path.basename(wav_path)}"
        )
        info.setObjectName("subheading")
        layout.addWidget(info)
        layout.addSpacing(12)

        # Buttons
        btn_layout = QHBoxLayout()

        btn_transcribe = QPushButton("Transcrire et Resumer")
        btn_transcribe.setObjectName("btn_gold")
        btn_transcribe.clicked.connect(lambda: self._choose(self.TRANSCRIBE))

        btn_rerecord = QPushButton("Re-enregistrer")
        btn_rerecord.clicked.connect(lambda: self._choose(self.RE_RECORD))

        btn_save = QPushButton("Sauvegarder sans transcrire")
        btn_save.clicked.connect(lambda: self._choose(self.SAVE_ONLY))

        btn_layout.addWidget(btn_transcribe)
        btn_layout.addWidget(btn_rerecord)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)

    def _choose(self, action):
        self.result_action = action
        self.accept()


class _VerticalDotsButton(QToolButton):
    """QToolButton that paints three bold, evenly-spaced vertical dots."""

    _DOT_RADIUS = 3
    _DOT_SPACING = 8

    def paintEvent(self, event):
        # Let QToolButton paint background / border via QSS
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Use the current text color from the stylesheet
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(self.palette().buttonText().color()))
        cx = self.width() / 2
        cy = self.height() / 2
        for offset in (-self._DOT_SPACING, 0, self._DOT_SPACING):
            p.drawEllipse(QRectF(
                cx - self._DOT_RADIUS, cy + offset - self._DOT_RADIUS,
                self._DOT_RADIUS * 2, self._DOT_RADIUS * 2,
            ))
        p.end()


class SessionTab(QWidget):
    """Recording, transcription, and summarization UI."""

    def __init__(self, config: dict, journal_widget=None, quest_log_widget=None, tts_engine=None, parent=None):
        super().__init__(parent)
        self._config = config
        self._journal = journal_widget
        self._quest_log = quest_log_widget
        self._tts_engine = tts_engine
        self._recorder = AudioRecorder(config, self)
        self._transcription_thread = None
        self._transcription_worker = None
        self._summary_thread = None
        self._summary_worker = None
        self._quest_thread = None
        self._quest_worker = None
        self._current_wav_path = None
        self._current_transcript = ""
        self._current_summary = ""
        self._elapsed = 0
        self._pulse_timer = None
        self._pulse_state = 0

        # Live transcription state
        self._live_transcript_parts = []
        self._last_live_transcription = 0.0
        self._live_tx_thread = None
        self._live_tx_worker = None
        self._live_tx_pending = False
        self._stop_after_current = False
        self._is_final_live_chunk = False

        self._build_ui()
        self._connect_signals()
        self._init_tts()
        self._init_recording_effects()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # === Recording Controls ===
        rec_layout = QHBoxLayout()

        self.btn_record = QPushButton("Enregistrer")
        self.btn_record.setObjectName("btn_record")

        self.btn_stop = QPushButton("Arrêter")
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.setEnabled(False)

        self.duration_label = QLabel("00:00:00")
        self.duration_label.setObjectName("duration_label")
        self.duration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        rec_layout.addWidget(self.btn_record)
        rec_layout.addWidget(self.btn_stop)
        rec_layout.addWidget(self.duration_label)
        layout.addLayout(rec_layout)

        # VU Meter
        self.vu_meter = QProgressBar()
        self.vu_meter.setRange(0, 100)
        self.vu_meter.setValue(0)
        self.vu_meter.setTextVisible(False)
        self.vu_meter.setMaximumHeight(12)
        layout.addWidget(self.vu_meter)

        # Status
        self.status_label = QLabel("Prêt à enregistrer")
        self.status_label.setObjectName("status_label")
        layout.addWidget(self.status_label)

        # ── Ornate divider: Recording ↔ Transcript ──
        layout.addWidget(_make_divider())

        # === Transcript ===
        transcript_label = QLabel("Transcription")
        transcript_label.setObjectName("subheading")
        layout.addWidget(transcript_label)

        self.transcript_display = QTextEdit()
        self.transcript_display.setObjectName("transcript_display")
        self.transcript_display.setReadOnly(True)
        self.transcript_display.setPlaceholderText("La transcription apparaitra ici après l'enregistrement...")
        self.transcript_display.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.transcript_display.customContextMenuRequested.connect(
            lambda pos: self._tts_context_menu(self.transcript_display, pos)
        )
        layout.addWidget(self.transcript_display)

        # ── Ornate divider: Transcript ↔ Summary ──
        layout.addWidget(_make_divider())

        # === Summary ===
        summary_header = QHBoxLayout()
        summary_label = QLabel("Resumé Épique")
        summary_label.setObjectName("subheading")
        summary_header.addWidget(summary_label)

        self.btn_tts = QPushButton("\U0001f50a")
        self.btn_tts.setToolTip("Lire le resumé à voix haute")
        self.btn_tts.setFixedWidth(36)
        self.btn_tts.setEnabled(False)
        summary_header.addWidget(self.btn_tts)
        summary_header.addStretch()
        layout.addLayout(summary_header)

        self.summary_display = QTextEdit()
        self.summary_display.setObjectName("summary_display")
        self.summary_display.setReadOnly(True)
        self.summary_display.setPlaceholderText("Le resumé épique apparaitra ici...")
        self.summary_display.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.summary_display.customContextMenuRequested.connect(
            lambda pos: self._tts_context_menu(self.summary_display, pos)
        )
        layout.addWidget(self.summary_display)

        # ── Ornate divider: Summary ↔ Actions ──
        layout.addWidget(_make_divider())

        # === Action Buttons ===
        action_layout = QHBoxLayout()

        self.btn_transcribe = QPushButton("Transcrire et Resumer")
        self.btn_transcribe.setObjectName("btn_primary")
        self.btn_transcribe.setEnabled(False)

        self.btn_add_journal = QPushButton("Ajouter au Journal")
        self.btn_add_journal.setObjectName("btn_gold")
        self.btn_add_journal.setEnabled(False)

        self.btn_update_quests = QPushButton("Mettre à jour les Quêtes")
        self.btn_update_quests.setObjectName("btn_gold")
        self.btn_update_quests.setEnabled(False)

        # Overflow menu for secondary actions
        self._more_menu = QMenu(self)
        self._act_import = self._more_menu.addAction("Importer un audio")
        self._act_save_audio = self._more_menu.addAction("Sauvegarder l'audio")
        self._act_save_audio.setEnabled(False)
        self._more_menu.addSeparator()
        self._act_copy = self._more_menu.addAction("Copier le resumé")
        self._act_copy.setEnabled(False)

        self.btn_more = _VerticalDotsButton()
        self.btn_more.setObjectName("btn_more")
        self.btn_more.setText("")
        self.btn_more.setToolTip("Plus d'options")
        self.btn_more.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.btn_more.setMenu(self._more_menu)

        action_layout.addWidget(self.btn_transcribe)
        action_layout.addWidget(self.btn_add_journal)
        action_layout.addWidget(self.btn_update_quests)
        action_layout.addWidget(self.btn_more)
        layout.addLayout(action_layout)

    def _connect_signals(self):
        self.btn_record.clicked.connect(self._on_record_btn_clicked)
        self.btn_stop.clicked.connect(self._stop_recording)
        self.btn_transcribe.clicked.connect(self._start_transcription)
        self.btn_add_journal.clicked.connect(self._add_to_journal)
        self.btn_update_quests.clicked.connect(self._start_quest_extraction)
        self.btn_tts.clicked.connect(self._speak_summary)

        # Overflow menu actions
        self._act_import.triggered.connect(self._import_audio)
        self._act_save_audio.triggered.connect(self._save_audio)
        self._act_copy.triggered.connect(self._copy_summary)

        self._recorder.recording_started.connect(self._on_recording_started)
        self._recorder.recording_stopped.connect(self._on_recording_stopped)
        self._recorder.recording_paused.connect(self._on_recording_paused)
        self._recorder.recording_resumed.connect(self._on_recording_resumed)
        self._recorder.level_update.connect(self._on_level_update)
        self._recorder.duration_update.connect(self._on_duration_update)
        self._recorder.error_occurred.connect(self._on_error)
        self._recorder.silence_detected.connect(self._on_silence_detected)

    def _init_tts(self):
        """Wire up the shared TTS engine signals."""
        if self._tts_engine:
            self._tts_engine.available.connect(self._on_tts_available)
            self._tts_engine.finished.connect(lambda: self.btn_tts.setEnabled(True))
            # Engine may already be initialized if thread started before us
            if self._tts_engine.is_available:
                self._on_tts_available(True)

    def _init_recording_effects(self):
        """Set up recording atmosphere overlays."""
        # Snowflake particles
        self._snow_overlay = SnowParticleOverlay(self, num_particles=12)
        self._snow_overlay.hide()

        # Aurora shimmer
        self._aurora_overlay = AuroraShimmerOverlay(self)
        self._aurora_overlay.hide()

        # Pulse glow timer for record button (slow breathing)
        self._pulse_timer = QTimer(self)
        self._pulse_timer.setInterval(1500)
        self._pulse_timer.timeout.connect(self._pulse_record_button)
        self._pulse_state = 0  # 3-state cycle: 0, 1, 2

    def _on_tts_available(self, available: bool):
        if not available:
            self.btn_tts.setToolTip("Aucune voix française disponible")

    # --- Recording ---

    def _on_record_btn_clicked(self):
        """Handle the record/pause/resume button click based on current state."""
        if not self._recorder.is_recording:
            self._recorder.start_recording()
        elif self._recorder.is_paused:
            self._recorder.resume_recording()
        else:
            self._recorder.pause_recording()

    def _stop_recording(self):
        self._recorder.stop_recording()

    def _on_recording_started(self):
        # Switch button to Pause mode
        self.btn_record.setText("Pause")
        self.btn_record.setObjectName("btn_pause")
        self.btn_record.style().unpolish(self.btn_record)
        self.btn_record.style().polish(self.btn_record)
        self.btn_record.setEnabled(True)
        self.btn_stop.setEnabled(True)
        self.btn_transcribe.setEnabled(False)
        self.transcript_display.clear()
        self.status_label.setText("Enregistrement en cours...")
        self.status_label.setStyleSheet("color: #ff6b6b;")

        # Reset live transcription state
        self._live_transcript_parts = []
        self._last_live_transcription = 0.0
        self._live_tx_pending = False
        self._stop_after_current = False
        self._is_final_live_chunk = False

        # Start recording atmosphere
        self._pulse_state = 0
        self._pulse_timer.start()
        self._snow_overlay.start()
        self._aurora_overlay.start()

    def _on_recording_paused(self):
        """Switch button to Resume mode."""
        self.btn_record.setText("Reprendre")
        self.btn_record.setObjectName("btn_resume")
        self.btn_record.style().unpolish(self.btn_record)
        self.btn_record.style().polish(self.btn_record)
        self.status_label.setText("Enregistrement en pause")
        self.status_label.setStyleSheet("color: #e8a824;")

        # Pause atmosphere effects
        self._pulse_timer.stop()
        self.btn_record.setStyleSheet("")
        self._snow_overlay.stop()
        self._aurora_overlay.stop()

    def _on_recording_resumed(self):
        """Switch button back to Pause mode."""
        self.btn_record.setText("Pause")
        self.btn_record.setObjectName("btn_pause")
        self.btn_record.style().unpolish(self.btn_record)
        self.btn_record.style().polish(self.btn_record)
        self.status_label.setText("Enregistrement en cours...")
        self.status_label.setStyleSheet("color: #ff6b6b;")

        # Resume atmosphere effects
        self._pulse_state = 0
        self._pulse_timer.start()
        self._snow_overlay.start()
        self._aurora_overlay.start()

    def _on_recording_stopped(self, wav_path: str):
        # Restore button to Record mode
        self.btn_record.setText("Enregistrer")
        self.btn_record.setObjectName("btn_record")
        self.btn_record.style().unpolish(self.btn_record)
        self.btn_record.style().polish(self.btn_record)
        self.btn_record.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.vu_meter.setValue(0)
        self._current_wav_path = wav_path

        # Stop recording atmosphere
        self._pulse_timer.stop()
        self.btn_record.setStyleSheet("")
        self._snow_overlay.stop()
        self._aurora_overlay.stop()

        if self._live_transcript_parts or self._live_tx_pending:
            # Live transcription was active — finalize automatically
            self.status_label.setText("Finalisation de la transcription...")
            self.status_label.setStyleSheet("color: #d4af37;")

            if self._live_tx_pending:
                # A chunk is still being transcribed — queue finalization
                self._stop_after_current = True
            else:
                self._do_final_live_transcription()
        else:
            # No live transcription happened — original dialog flow
            self.status_label.setText("Enregistrement terminé")
            self.status_label.setStyleSheet("color: #7ec8e3;")

            dlg = PostRecordingDialog(wav_path, self._elapsed, self)
            dlg.exec()

            if dlg.result_action == PostRecordingDialog.TRANSCRIBE:
                self._start_transcription()
            elif dlg.result_action == PostRecordingDialog.RE_RECORD:
                self.status_label.setText("Prêt à re-enregistrer")
                self.duration_label.setText("00:00:00")
            else:
                self.btn_transcribe.setEnabled(True)
                self._act_save_audio.setEnabled(True)
                self.status_label.setText("Enregistrement sauvegardé")

    def _pulse_record_button(self):
        """Cycle the pause button border through 3 states (slow breathing)."""
        colors = ["#8a5a10", "#c48820", "#e8a824"]
        self._pulse_state = (self._pulse_state + 1) % 3
        color = colors[self._pulse_state]
        obj = self.btn_record.objectName()
        self.btn_record.setStyleSheet(f"QPushButton#{obj} {{ border: 2px solid {color}; }}")

    def _import_audio(self):
        """Import an existing audio file for transcription."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Importer un fichier audio",
            "",
            "Fichiers audio (*.wav *.mp3 *.flac *.ogg *.m4a *.wma);;Tous (*)",
        )
        if not file_path:
            return

        # Create a session folder and copy the file there
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_folder = os.path.join(sessions_dir(self._config), f"session_{ts}_import")
        ensure_dir(session_folder)

        dest_name = os.path.basename(file_path)
        dest_path = os.path.join(session_folder, dest_name)
        try:
            shutil.copy2(file_path, dest_path)
        except OSError as e:
            self._on_error(f"Erreur lors de la copie: {e}")
            return

        self._current_wav_path = dest_path
        self.btn_transcribe.setEnabled(True)
        self._act_save_audio.setEnabled(True)

        size = os.path.getsize(dest_path)
        self.status_label.setText(f"Audio importé: {dest_name} ({format_file_size(size)})")
        self.status_label.setStyleSheet("color: #7ec8e3;")

    def _save_audio(self):
        """Save the audio as FLAC (converting from source if needed)."""
        src_path = self._current_wav_path or self._recorder.wav_path
        if not src_path or not os.path.exists(src_path):
            self._on_error("Aucun fichier audio à sauvegarder.")
            return

        session_dir = os.path.dirname(src_path)
        flac_path = os.path.join(session_dir, "full_audio.flac")

        # Convert to FLAC if not already done (e.g. before transcription)
        if not os.path.exists(flac_path):
            try:
                data, sr = sf.read(src_path, dtype="int16")
                sf.write(flac_path, data, sr, format="FLAC")
            except Exception as e:
                self._on_error(f"Erreur de conversion FLAC: {e}")
                return

        base = os.path.splitext(os.path.basename(src_path))[0]
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Sauvegarder le fichier audio",
            f"{base}.flac",
            "FLAC (*.flac);;Tous (*)",
        )
        if not save_path:
            return

        try:
            shutil.copy2(flac_path, save_path)
            self.status_label.setText(f"Audio sauvegardé: {os.path.basename(save_path)}")
            self.status_label.setStyleSheet("color: #7ec83a;")
        except OSError as e:
            self._on_error(f"Erreur de sauvegarde: {e}")

    def _on_level_update(self, level: float):
        self.vu_meter.setValue(int(level * 100))

    def _on_duration_update(self, seconds: int):
        self._elapsed = seconds
        self.duration_label.setText(format_duration(seconds))

    # --- Transcription ---

    def _start_transcription(self):
        wav_path = self._current_wav_path or self._recorder.wav_path
        if not wav_path or not os.path.exists(wav_path):
            self._on_error("Aucun fichier audio trouvé.")
            return

        self.status_label.setText("Transcription en cours...")
        self.status_label.setStyleSheet("color: #d4af37;")
        self.btn_transcribe.setEnabled(False)
        self.transcript_display.clear()

        self._transcription_thread, self._transcription_worker = start_transcription(wav_path, self._config)
        self._transcription_worker.progress.connect(self._on_transcription_progress)
        self._transcription_worker.chunk_completed.connect(self._on_chunk_completed)
        self._transcription_worker.completed.connect(self._on_transcription_done)
        self._transcription_worker.error.connect(self._on_error)
        self._transcription_thread.start()

    # --- Live transcription (during recording) ---

    def _on_silence_detected(self):
        """Trigger live transcription when silence is detected during recording."""
        if not self._recorder.is_recording:
            return
        if self._live_tx_pending:
            return  # already transcribing a chunk
        now = time.time()
        if now - self._last_live_transcription < 60:
            return  # respect 60s cooldown

        flac_path = self._recorder.flush_pending_audio()
        if not flac_path:
            return

        self._last_live_transcription = now
        self._live_tx_pending = True
        self._is_final_live_chunk = False

        self._live_tx_thread, self._live_tx_worker = start_live_transcription(
            flac_path, self._config
        )
        self._live_tx_worker.completed.connect(self._on_live_tx_done)
        self._live_tx_worker.error.connect(self._on_live_tx_error)
        self._live_tx_thread.start()

        count = len(self._live_transcript_parts) + 1
        self.status_label.setText(f"Transcription du segment {count}...")
        self.status_label.setStyleSheet("color: #d4af37;")

    def _do_final_live_transcription(self):
        """Transcribe remaining audio after recording stopped."""
        remaining = self._recorder.flush_pending_audio()
        if remaining:
            self._is_final_live_chunk = True
            self._live_tx_pending = True

            self._live_tx_thread, self._live_tx_worker = start_live_transcription(
                remaining, self._config
            )
            self._live_tx_worker.completed.connect(self._on_live_tx_done)
            self._live_tx_worker.error.connect(self._on_live_tx_error)
            self._live_tx_thread.start()
        else:
            self._finalize_live_transcription()

    def _on_live_tx_done(self, text: str):
        """Handle a completed live transcription chunk."""
        self._live_tx_pending = False
        if text.strip():
            self._live_transcript_parts.append(text)
            self.transcript_display.append(text)

        if self._is_final_live_chunk:
            self._is_final_live_chunk = False
            self._finalize_live_transcription()
        elif self._stop_after_current:
            # Recording stopped while we were transcribing — now do the final flush
            self._stop_after_current = False
            self._do_final_live_transcription()
        else:
            count = len(self._live_transcript_parts)
            self.status_label.setText(
                f"Enregistrement... ({count} segment{'s' if count > 1 else ''} transcrit{'s' if count > 1 else ''})"
            )
            self.status_label.setStyleSheet("color: #ff6b6b;")

    def _on_live_tx_error(self, msg: str):
        """Handle live transcription error — continue recording."""
        self._live_tx_pending = False
        self.status_label.setText(f"Erreur transcription: {msg}")
        self.status_label.setStyleSheet("color: #ff6b6b;")

        if self._is_final_live_chunk:
            self._is_final_live_chunk = False
            self._finalize_live_transcription()
        elif self._stop_after_current:
            self._stop_after_current = False
            self._do_final_live_transcription()

    def _finalize_live_transcription(self):
        """Combine all live transcript parts and proceed to summarization."""
        full_text = "\n\n".join(self._live_transcript_parts)
        self._current_transcript = full_text
        self.transcript_display.setPlainText(full_text)

        # Save transcript to session directory
        if self._current_wav_path:
            session_dir = os.path.dirname(self._current_wav_path)
            transcript_path = os.path.join(session_dir, "transcript.txt")
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(full_text)

        self._act_save_audio.setEnabled(True)
        self.btn_transcribe.setEnabled(True)

        if full_text.strip():
            self.status_label.setText("Transcription terminée. Génération du résumé...")
            self.status_label.setStyleSheet("color: #d4af37;")
            self._start_summarization()
        else:
            self.status_label.setText("Aucun texte transcrit.")
            self.status_label.setStyleSheet("color: #7ec8e3;")

    # --- Batch transcription (post-recording) ---

    def _on_transcription_progress(self, current: int, total: int):
        self.status_label.setText(f"Transcription: chunk {current}/{total}...")

    def _on_chunk_completed(self, index: int, text: str):
        self.transcript_display.append(text)

    def _on_transcription_done(self, full_text: str):
        self._current_transcript = full_text
        self.transcript_display.setPlainText(full_text)
        self.status_label.setText("Transcription terminée. Génération du résumé...")
        self._start_summarization()

    # --- Summarization ---

    def _start_summarization(self):
        # Combine journal (narrative flow) and quest log (active quest state)
        journal_context = ""
        if self._journal:
            journal_context = self._journal.get_compact_context()

        quest_context = ""
        if self._quest_log:
            quest_context = self._quest_log.get_compact_context()

        # Build combined context
        context_parts = []
        if journal_context:
            context_parts.append(f"=== Journal (récits précédents) ===\n{journal_context}")
        if quest_context:
            context_parts.append(f"=== Quest Log (quêtes actives) ===\n{quest_context}")
        combined_context = "\n\n".join(context_parts)

        self._summary_thread, self._summary_worker = start_summarization(
            self._current_transcript, combined_context, self._config
        )
        self._summary_worker.completed.connect(self._on_summary_done)
        self._summary_worker.error.connect(self._on_error)
        self._summary_thread.start()

    def _on_summary_done(self, summary_html: str):
        self._current_summary = summary_html
        self.summary_display.setHtml(summary_html)
        self.status_label.setText("Resumé généré !")
        self.status_label.setStyleSheet("color: #7ec83a;")
        self._act_copy.setEnabled(True)
        self.btn_add_journal.setEnabled(True)
        self.btn_update_quests.setEnabled(True)
        self.btn_transcribe.setEnabled(True)
        self._act_save_audio.setEnabled(bool(self._current_wav_path or self._recorder.wav_path))
        if self._tts_engine.is_available:
            self.btn_tts.setEnabled(True)

    # --- Actions ---

    def _copy_summary(self):
        if self._current_summary:
            clipboard = QApplication.clipboard()
            clipboard.setText(self._current_summary)
            self.status_label.setText("Resumé copié dans le presse-papiers !")

    def _add_to_journal(self):
        if self._current_summary and self._journal:
            self._journal.append_summary(self._current_summary)
            self.status_label.setText("Resumé ajouté au Journal !")
            self.status_label.setStyleSheet("color: #d4af37;")
            self.btn_add_journal.setEnabled(False)

    def _start_quest_extraction(self):
        if not self._current_summary:
            return

        current_quests = ""
        if self._quest_log:
            current_quests = self._quest_log.editor.toPlainText()

        self.status_label.setText("Extraction des quêtes en cours...")
        self.status_label.setStyleSheet("color: #d4af37;")
        self.btn_update_quests.setEnabled(False)

        self._quest_thread, self._quest_worker = start_quest_extraction(
            self._current_summary, current_quests, self._config
        )
        self._quest_worker.completed.connect(self._on_quest_extraction_done)
        self._quest_worker.error.connect(self._on_error)
        self._quest_thread.start()

    def _on_quest_extraction_done(self, proposed_html: str):
        self.status_label.setText("Propositions de quêtes prêtes.")
        self.status_label.setStyleSheet("color: #7ec83a;")

        current_html = self._quest_log.get_full_html() if self._quest_log else ""
        dlg = QuestProposalDialog(proposed_html, current_html, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            edited_html = dlg.get_html()
            if self._quest_log:
                self._quest_log.replace_quest_log(edited_html)
                self.status_label.setText("Quêtes mises a jour !")
                self.status_label.setStyleSheet("color: #d4af37;")
        else:
            self.status_label.setText("Mise a jour des quêtes annulée.")
            self.btn_update_quests.setEnabled(True)

    def _tts_context_menu(self, editor: QTextEdit, pos):
        """Show context menu with TTS option for selected text."""
        menu = editor.createStandardContextMenu()
        selection = editor.textCursor().selectedText()
        if selection and self._tts_engine and self._tts_engine.is_available:
            menu.addSeparator()
            tts_action = QAction("Lire la sélection", menu)
            tts_action.triggered.connect(lambda _checked=False, t=selection: self._speak_text(t))
            menu.addAction(tts_action)
        menu.exec(editor.mapToGlobal(pos))

    def _speak_text(self, text: str):
        """Speak arbitrary text via the shared TTS engine."""
        if text and self._tts_engine and self._tts_engine.is_available:
            self._tts_engine.speak_requested.emit(text)

    def _speak_summary(self):
        if self._current_summary and self._tts_engine and self._tts_engine.is_available:
            self.btn_tts.setEnabled(False)
            self._tts_engine.speak_requested.emit(self._current_summary)

    def _on_error(self, msg: str):
        self.status_label.setText(msg)
        self.status_label.setStyleSheet("color: #ff6b6b;")
        # Restore record button to initial state
        self.btn_record.setText("Enregistrer")
        self.btn_record.setObjectName("btn_record")
        self.btn_record.style().unpolish(self.btn_record)
        self.btn_record.style().polish(self.btn_record)
        self.btn_record.setStyleSheet("")
        self.btn_record.setEnabled(True)
        self.btn_stop.setEnabled(False)
        has_audio = bool(self._current_wav_path or self._recorder.wav_path)
        self.btn_transcribe.setEnabled(has_audio)
        self._act_save_audio.setEnabled(has_audio)
        self.btn_update_quests.setEnabled(bool(self._current_summary))

    def cleanup(self):
        """Clean up threads and temporary FLAC files on exit."""
        # Remove FLAC files generated during transcription
        self._cleanup_flac_files()

        # Stop recording effects
        if self._pulse_timer:
            self._pulse_timer.stop()
        if self._snow_overlay:
            self._snow_overlay.stop()
        if self._aurora_overlay:
            self._aurora_overlay.stop()

        # TTS engine is shared and cleaned up by IcewindDaleApp
        if self._live_tx_thread and self._live_tx_thread.isRunning():
            self._live_tx_thread.quit()
            self._live_tx_thread.wait(2000)
        if self._transcription_thread and self._transcription_thread.isRunning():
            self._transcription_thread.quit()
            self._transcription_thread.wait(2000)
        if self._summary_thread and self._summary_thread.isRunning():
            self._summary_thread.quit()
            self._summary_thread.wait(2000)
        if self._quest_thread and self._quest_thread.isRunning():
            self._quest_thread.quit()
            self._quest_thread.wait(2000)

    def _cleanup_flac_files(self):
        """Remove temporary FLAC files from the current session directory."""
        wav_path = self._current_wav_path or getattr(self._recorder, "wav_path", None)
        if not wav_path:
            return
        session_dir = os.path.dirname(wav_path)
        for flac_file in glob.glob(os.path.join(session_dir, "*.flac")):
            try:
                os.remove(flac_file)
            except OSError:
                pass

    def update_config(self, config: dict):
        """Update config after settings change."""
        self._config = config
