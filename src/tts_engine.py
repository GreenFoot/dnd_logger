"""Text-to-Speech engine using edge-tts for high-quality French narration.

Splits text into sentences and pipelines generation with playback:
sentence N+1 is generated in a background thread while sentence N plays,
so the only gap between sentences is the player open/play overhead.

Playback backend is platform-specific: Windows MCI (winmm) on Windows,
the built-in ``afplay`` command on macOS.
"""

import asyncio
import ctypes
import html
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time

from PySide6.QtCore import QObject, QThread, Signal, Slot

from .i18n import tr


class _MciPlayer:
    """Plays an MP3 file through Windows MCI (winmm).

    MCI aliases are thread-local, so every method must be called from the same thread.
    """

    def __init__(self):
        self._winmm = ctypes.windll.winmm

    def _send(self, command: str) -> str:
        buf = ctypes.create_unicode_buffer(256)
        self._winmm.mciSendStringW(command, buf, 256, None)
        return buf.value

    def play(self, path: str):
        """Open and start playing a file."""
        self._send(f'open "{path}" type mpegvideo alias tts_clip')
        self._send("play tts_clip")

    def pause(self):
        """Pause the current clip."""
        self._send("pause tts_clip")

    def resume(self):
        """Resume the current clip."""
        self._send("resume tts_clip")

    def is_done(self) -> bool:
        """Return whether the current clip has finished playing."""
        return self._send("status tts_clip mode") in ("stopped", "")

    def close(self):
        """Stop and release the current clip."""
        self._send("stop tts_clip")
        self._send("close tts_clip")


class _AfplayPlayer:
    """Plays an MP3 file through macOS ``afplay``, pausing with SIGSTOP/SIGCONT."""

    def __init__(self):
        if not shutil.which("afplay"):
            raise OSError("afplay not found")
        self._proc = None

    def play(self, path: str):
        """Start playing a file."""
        self._proc = subprocess.Popen(["afplay", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def pause(self):
        """Pause the current clip."""
        if self._proc and self._proc.poll() is None:
            self._proc.send_signal(signal.SIGSTOP)

    def resume(self):
        """Resume the current clip."""
        if self._proc and self._proc.poll() is None:
            self._proc.send_signal(signal.SIGCONT)

    def is_done(self) -> bool:
        """Return whether the current clip has finished playing."""
        return self._proc is None or self._proc.poll() is not None

    def close(self):
        """Stop the current clip."""
        if self._proc and self._proc.poll() is None:
            self._proc.send_signal(signal.SIGCONT)
            self._proc.terminate()
            try:
                self._proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self._proc.kill()
        self._proc = None


def _create_player():
    """Return an audio player for the current platform."""
    if sys.platform == "win32":
        return _MciPlayer()
    if sys.platform == "darwin":
        return _AfplayPlayer()
    raise OSError(f"No TTS playback backend for {sys.platform}")


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
    _SENTENCE_RE = re.compile(r"(?<=[.!?…])\s+|\n+")

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_available = False
        self._playing = False
        self._paused = False
        self._stop_requested = False
        self._player = None
        self.speak_requested.connect(self._on_speak)

    def init_engine(self):
        """Check that edge-tts is importable. Call from worker thread."""
        try:
            import edge_tts  # noqa: F401

            self._player = _create_player()
            self._is_available = True
            self.available.emit(True)
        except Exception:
            self._is_available = False
            self.available.emit(False)

    @property
    def is_available(self) -> bool:
        """Return whether the TTS engine is ready."""
        return self._is_available

    @property
    def is_speaking(self) -> bool:
        """Return whether audio is currently playing."""
        return self._playing

    @property
    def is_paused(self) -> bool:
        """Return whether playback is paused."""
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
            self.error.emit(tr("tts.error.unavailable"))
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
                self._player.play(current_path)

                _was_paused = False
                while not self._stop_requested:
                    # Handle pause/resume from the worker thread
                    # (MCI aliases are thread-local on Windows)
                    if self._paused and not _was_paused:
                        self._player.pause()
                        _was_paused = True
                    elif not self._paused and _was_paused:
                        self._player.resume()
                        _was_paused = False

                    if self._player.is_done():
                        break
                    time.sleep(0.02)

                self._player.close()
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
                self.error.emit(tr("tts.error.generic", error=e))
            else:
                self.finished.emit()

    def pause(self):
        """Request pause. The worker thread applies it to the player."""
        if self._playing and not self._paused:
            self._paused = True
            self.paused.emit()

    def resume(self):
        """Request resume. The worker thread applies it to the player."""
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
