"""Text-to-Speech engine using edge-tts for high-quality French narration.

Splits text into sentences and pipelines generation with playback:
sentence N+1 is generated in a background thread while sentence N plays,
so the only gap between sentences is the MCI open/play overhead (~10ms).
"""

import asyncio
import ctypes
import html
import os
import re
import tempfile
import threading
import time

from PySide6.QtCore import QObject, QThread, Signal, Slot


class TTSEngine(QObject):
    """TTS playback using Microsoft Edge TTS in a background thread.

    While one sentence plays, the next sentence's audio is generated
    in parallel so transitions are nearly instantaneous.
    """

    started = Signal()
    finished = Signal()
    paused = Signal()
    resumed = Signal()
    error = Signal(str)
    available = Signal(bool)
    speak_requested = Signal(str)

    VOICE = "fr-FR-RemyMultilingualNeural"

    # Split on sentence-ending punctuation followed by whitespace, or on newlines
    _SENTENCE_RE = re.compile(r'(?<=[.!?…])\s+|\n+')

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_available = False
        self._playing = False
        self._paused = False
        self._stop_requested = False
        self._winmm = None
        self.speak_requested.connect(self._on_speak)

    def init_engine(self):
        """Check that edge-tts is importable. Call from worker thread."""
        try:
            import edge_tts  # noqa: F401
            self._winmm = ctypes.windll.winmm
            self._is_available = True
            self.available.emit(True)
        except Exception:
            self._is_available = False
            self.available.emit(False)

    @property
    def is_available(self) -> bool:
        return self._is_available

    @property
    def is_speaking(self) -> bool:
        return self._playing

    @property
    def is_paused(self) -> bool:
        return self._paused

    def _clean_text(self, text: str) -> str:
        """Strip HTML tags and normalize whitespace."""
        clean = re.sub(r"<[^>]+>", " ", text)
        clean = html.unescape(clean)
        clean = re.sub(r"\s+", " ", clean).strip()
        return clean

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences for incremental playback."""
        sentences = self._SENTENCE_RE.split(text)
        result = []
        for s in sentences:
            s = s.strip()
            if not s:
                continue
            # Merge very short fragments with the previous sentence
            if result and len(s) < 10:
                result[-1] = result[-1] + " " + s
            else:
                result.append(s)
        return result

    @staticmethod
    def _new_tmp() -> str:
        """Create a new temporary MP3 file and return its path."""
        tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        path = tmp.name
        tmp.close()
        return path

    @staticmethod
    def _safe_unlink(path: str | None):
        """Delete a file, ignoring errors."""
        if path:
            try:
                os.unlink(path)
            except OSError:
                pass

    def _generate_audio(self, sentence: str, path: str):
        """Generate MP3 for a single sentence (blocking network call)."""
        import edge_tts
        communicate = edge_tts.Communicate(sentence, self.VOICE)
        asyncio.run(communicate.save(path))

    def _bg_generate(self, sentence: str, result: list):
        """Background thread: generate audio only. result = [path, error]."""
        try:
            self._generate_audio(sentence, result[0])
        except Exception as e:
            result[1] = e

    @Slot(str)
    def _on_speak(self, text: str):
        """Generate and play speech with pipelined sentence generation."""
        if not self._is_available:
            self.error.emit("TTS non disponible.")
            return
        try:
            clean = self._clean_text(text)
            if not clean:
                self.finished.emit()
                return

            self._stop_requested = False
            self._paused = False
            self.started.emit()

            sentences = self._split_sentences(clean)
            if not sentences:
                self.finished.emit()
                return

            # Generate first sentence synchronously (nothing to play yet)
            current_path = self._new_tmp()
            self._generate_audio(sentences[0], current_path)

            for i in range(len(sentences)):
                if self._stop_requested:
                    self._safe_unlink(current_path)
                    break

                # Respect pause between sentences
                while self._paused and not self._stop_requested:
                    time.sleep(0.05)

                if self._stop_requested:
                    self._safe_unlink(current_path)
                    break

                # Pipeline: start generating next sentence in background
                bg_thread = None
                next_result = [None, None]  # [path, error]
                if i + 1 < len(sentences) and not self._stop_requested:
                    next_result[0] = self._new_tmp()
                    bg_thread = threading.Thread(
                        target=self._bg_generate,
                        args=(sentences[i + 1], next_result),
                        daemon=True,
                    )
                    bg_thread.start()

                # Play current sentence (non-blocking + poll)
                self._playing = True
                self._mci(f'open "{current_path}" type mpegvideo alias tts_clip')
                self._mci("play tts_clip")

                _was_paused = False
                while not self._stop_requested:
                    # Handle pause/resume from the worker thread
                    # (MCI aliases are thread-local on Windows)
                    if self._paused and not _was_paused:
                        self._mci("pause tts_clip")
                        _was_paused = True
                    elif not self._paused and _was_paused:
                        self._mci("resume tts_clip")
                        _was_paused = False

                    mode = self._mci_query("status tts_clip mode")
                    if mode in ("stopped", ""):
                        break
                    time.sleep(0.02)

                self._mci("stop tts_clip")
                self._mci("close tts_clip")
                self._playing = False
                self._safe_unlink(current_path)

                # Wait for background generation if still running
                if bg_thread:
                    bg_thread.join(timeout=30)

                if self._stop_requested:
                    self._safe_unlink(next_result[0])
                    break

                if next_result[1]:
                    # Generation failed — skip that sentence
                    self._safe_unlink(next_result[0])
                    continue

                # Advance: next becomes current
                current_path = next_result[0]

            self.finished.emit()

        except Exception as e:
            self._playing = False
            if not self._stop_requested:
                self.error.emit(f"Erreur TTS: {e}")
            else:
                self.finished.emit()

    def _mci(self, command: str):
        """Send an MCI command string."""
        if self._winmm:
            self._winmm.mciSendStringW(command, None, 0, None)

    def _mci_query(self, command: str) -> str:
        """Send an MCI query and return the result string."""
        if self._winmm:
            buf = ctypes.create_unicode_buffer(256)
            self._winmm.mciSendStringW(command, buf, 256, None)
            return buf.value
        return ""

    def pause(self):
        """Request pause. The worker thread applies the MCI command."""
        if self._playing and not self._paused:
            self._paused = True
            self.paused.emit()

    def resume(self):
        """Request resume. The worker thread applies the MCI command."""
        if self._paused:
            self._paused = False
            self.resumed.emit()

    def stop(self):
        """Request stop. The worker thread closes the clip."""
        self._stop_requested = True
        self._paused = False


def create_tts_thread() -> tuple[QThread, TTSEngine]:
    """Create a TTS engine in its own thread."""
    thread = QThread()
    engine = TTSEngine()
    engine.moveToThread(thread)
    thread.started.connect(engine.init_engine)
    return thread, engine
