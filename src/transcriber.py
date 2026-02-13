"""Audio chunking and Mistral Voxtral transcription pipeline."""

import math
import os
import re
import time

import soundfile as sf
from PyQt6.QtCore import QObject, QThread, pyqtSignal

from .utils import load_config


class AudioChunker:
    """Splits a WAV file into chunks if it exceeds max duration."""

    @staticmethod
    def chunk_audio(wav_path: str, max_minutes: int = 150) -> list[str]:
        """Split WAV into chunks with 10s overlap. Returns list of file paths."""
        info = sf.info(wav_path)
        total_seconds = info.duration
        max_seconds = max_minutes * 60

        sr = info.samplerate
        chunk_dir = os.path.dirname(wav_path)

        if total_seconds <= max_seconds:
            flac_path = os.path.join(chunk_dir, "full_audio.flac")
            data, _ = sf.read(wav_path, dtype="int16")
            sf.write(flac_path, data, sr, format="FLAC")
            return [flac_path]

        overlap_samples = int(10 * sr)
        chunk_samples = int(max_seconds * sr)

        chunks = []
        data, _ = sf.read(wav_path, dtype="int16")

        total_samples = len(data)
        start = 0
        idx = 0

        while start < total_samples:
            end = min(start + chunk_samples, total_samples)
            chunk_data = data[start:end]

            chunk_path = os.path.join(chunk_dir, f"chunk_{idx:03d}.flac")
            sf.write(chunk_path, chunk_data, sr, format="FLAC")
            chunks.append(chunk_path)

            idx += 1
            start = end - overlap_samples
            if end >= total_samples:
                break

        return chunks


def _transcribe_file(client, chunk_path: str, config: dict, retries: int = 3) -> str:
    """Transcribe a single audio file using Mistral Voxtral API with retry logic."""
    _BIAS_VALID = re.compile(r"^[a-zA-Z0-9_-]+$")
    raw_bias = config.get("context_bias", [])
    context_bias = []
    for b in raw_bias:
        entry = b.replace(" ", "_").replace("&", "")
        if entry and _BIAS_VALID.match(entry):
            context_bias.append(entry)
    language = config.get("language", "fr")

    model = config.get("transcription_model", "voxtral-mini-latest")
    diarize = config.get("diarize", False)

    for attempt in range(retries):
        try:
            with open(chunk_path, "rb") as f:
                kwargs = dict(
                    model=model,
                    file={"file_name": os.path.basename(chunk_path), "content": f},
                    language=language,
                    context_bias=context_bias or None,
                    diarize=diarize,
                )
                if diarize:
                    kwargs["timestamp_granularities"] = ["segment"]
                result = client.audio.transcriptions.complete(**kwargs)

            if diarize and hasattr(result, "segments") and result.segments:
                parts = []
                for seg in result.segments:
                    speaker = getattr(seg, "speaker", None)
                    text = getattr(seg, "text", str(seg))
                    if speaker is not None:
                        parts.append(f"[{speaker}]: {text}")
                    else:
                        parts.append(text)
                return "\n".join(parts)

            return result.text if hasattr(result, "text") else str(result)

        except Exception as e:
            err_str = str(e)
            if "401" in err_str:
                raise RuntimeError("Clé API invalide. Verifiez votre clé dans les Paramètres.")
            if "429" in err_str and attempt < retries - 1:
                wait = 2 ** (attempt + 1)
                time.sleep(wait)
                continue
            if attempt == retries - 1:
                raise
    return ""


class TranscriptionWorker(QObject):
    """Runs transcription in a QThread via Mistral Voxtral API."""

    progress = pyqtSignal(int, int)  # current, total
    chunk_completed = pyqtSignal(int, str)  # index, text
    completed = pyqtSignal(str)  # full transcript
    error = pyqtSignal(str)

    def __init__(self, wav_path: str, config: dict):
        super().__init__()
        self._wav_path = wav_path
        self._config = config

    def run(self):
        """Execute transcription pipeline."""
        try:
            from mistralai import Mistral

            api_key = self._config.get("api_key", "")
            if not api_key:
                self.error.emit("Clé API Mistral non configurée. Allez dans Paramètres.")
                return

            client = Mistral(api_key=api_key)
            max_minutes = self._config.get("chunk_duration_minutes", 150)
            chunks = AudioChunker.chunk_audio(self._wav_path, max_minutes)
            total = len(chunks)
            full_text_parts = []

            for i, chunk_path in enumerate(chunks):
                self.progress.emit(i + 1, total)
                text = _transcribe_file(client, chunk_path, self._config)
                full_text_parts.append(text)
                self.chunk_completed.emit(i, text)

            full_text = "\n\n".join(full_text_parts)

            # Save transcript
            session_dir = os.path.dirname(self._wav_path)
            transcript_path = os.path.join(session_dir, "transcript.txt")
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(full_text)

            self.completed.emit(full_text)

        except Exception as e:
            self.error.emit(f"Erreur de transcription: {e}")


class LiveTranscriptionWorker(QObject):
    """Transcribes a single audio chunk for live/incremental transcription."""

    completed = pyqtSignal(str)  # transcribed text
    error = pyqtSignal(str)

    def __init__(self, flac_path: str, config: dict):
        super().__init__()
        self._flac_path = flac_path
        self._config = config

    def run(self):
        try:
            from mistralai import Mistral

            api_key = self._config.get("api_key", "")
            if not api_key:
                self.error.emit("Clé API Mistral non configurée.")
                return

            client = Mistral(api_key=api_key)
            text = _transcribe_file(client, self._flac_path, self._config)

            # Clean up temp FLAC file
            try:
                os.remove(self._flac_path)
            except OSError:
                pass

            self.completed.emit(text)

        except Exception as e:
            self.error.emit(f"Erreur de transcription live: {e}")


def start_transcription(wav_path: str, config: dict) -> tuple[QThread, TranscriptionWorker]:
    """Create and start a transcription worker in a new thread."""
    thread = QThread()
    worker = TranscriptionWorker(wav_path, config)
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.completed.connect(thread.quit)
    worker.error.connect(thread.quit)
    return thread, worker


def start_live_transcription(flac_path: str, config: dict) -> tuple[QThread, LiveTranscriptionWorker]:
    """Create a live transcription worker in a new thread."""
    thread = QThread()
    worker = LiveTranscriptionWorker(flac_path, config)
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.completed.connect(thread.quit)
    worker.error.connect(thread.quit)
    return thread, worker
