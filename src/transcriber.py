"""Audio chunking and Mistral Voxtral transcription pipeline."""

import logging
import os
import re
import time

import numpy as np
import soundfile as sf
from PySide6.QtCore import QObject, QThread, Signal

from .i18n import tr
from .mistral_compat import mistral_class

log = logging.getLogger("dndlogger.transcriber")


def flac_stem(audio_path: str) -> str:
    """Return a filesystem-safe stem used to name the FLAC files derived from an audio file.

    Several source files can live in the same session directory, so chunk names are
    namespaced per source instead of using fixed ``full_audio.flac`` / ``chunk_NNN.flac``.

    Args:
        audio_path: Path of the source audio file.

    Returns:
        A sanitized stem, never empty.
    """
    stem = os.path.splitext(os.path.basename(audio_path))[0]
    stem = re.sub(r"[^A-Za-z0-9_-]+", "_", stem).strip("_")
    return stem or "audio"


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
        stem = flac_stem(wav_path)

        if total_seconds <= max_seconds:
            # Already a FLAC that fits in one request — upload it as-is.
            if os.path.splitext(wav_path)[1].lower() == ".flac":
                return [wav_path]
            flac_path = os.path.join(chunk_dir, f"{stem}__full.flac")
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

            chunk_path = os.path.join(chunk_dir, f"{stem}__chunk_{idx:03d}.flac")
            sf.write(chunk_path, chunk_data, sr, format="FLAC")
            chunks.append(chunk_path)

            idx += 1
            start = end - overlap_samples
            if end >= total_samples:
                break

        return chunks


def _strip_stt_artifacts(text: str, min_repeats: int = 5, min_words: int = 2, max_words: int = 15) -> str:
    """Collapse consecutive repetitions of a phrase that Voxtral sometimes emits in loops.

    A phrase of N words (min_words <= N <= max_words) repeated min_repeats times or more in
    immediate succession is reduced to two occurrences (kept rather than one to preserve
    legitimate doublings like "non, non").
    """
    for nwords in range(min_words, max_words + 1):
        pattern = re.compile(r"((?:\b\S+\b[^\w]*){" + str(nwords) + r"})(\1){" + str(min_repeats - 1) + r",}")
        text = pattern.sub(r"\1\1", text)
    return text


def _transcribe_file(client, chunk_path: str, config: dict, retries: int = 3) -> str:
    """Transcribe a single audio file using Mistral Voxtral API with retry logic."""
    _BIAS_VALID = re.compile(r"^[a-zA-Z0-9_-]+$")  # pylint: disable=invalid-name
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
                raise RuntimeError(tr("transcriber.error.invalid_key"))
            if "429" in err_str and attempt < retries - 1:
                wait = 15 * (2**attempt)  # 15s, 30s, 60s
                time.sleep(wait)
                continue
            if attempt == retries - 1:
                raise
    return ""


TRANSCRIPT_EXTENSIONS = {".txt", ".md", ".text"}


def is_transcript_file(path: str) -> bool:
    """Return True if path is an already-written transcript rather than audio."""
    return os.path.splitext(path)[1].lower() in TRANSCRIPT_EXTENSIONS


def read_transcript_file(path: str) -> str:
    """Read an existing transcript file, tolerating non-UTF-8 encodings.

    Transcripts written by other tools on Windows are often cp1252 rather than UTF-8,
    so fall back through the usual suspects instead of producing replacement chars.

    Args:
        path: Path of the transcript file.

    Returns:
        The file contents.
    """
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            with open(path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    # latin-1 maps every byte, so this last attempt cannot fail
    with open(path, "r", encoding="latin-1") as f:
        return f.read()


class TranscriptionWorker(QObject):
    """Runs transcription in a QThread via Mistral Voxtral API."""

    progress = Signal(int, int)  # current, total
    file_started = Signal(int, int, str)  # file index (1-based), file count, file name
    chunk_completed = Signal(int, str)  # index, text
    completed = Signal(str)  # full transcript
    error = Signal(str)

    def __init__(self, wav_paths, config: dict):
        """Initialize the worker.

        Args:
            wav_paths: A single file path, or a list of paths processed in the given
                order (one session recorded across several files). Audio files are
                transcribed; existing transcript files (.txt/.md) are inserted as-is,
                so audio and transcripts can be mixed freely in one batch.
            config: Campaign configuration dict.
        """
        super().__init__()
        self._wav_paths = [wav_paths] if isinstance(wav_paths, str) else list(wav_paths)
        self._config = config

    def run(self):
        """Build the session transcript from every input file, in order."""
        client = None
        try:
            max_minutes = self._config.get("chunk_duration_minutes", 150)
            paths = self._wav_paths

            # The API is only needed when at least one input is audio.
            if any(not is_transcript_file(path) for path in paths):
                api_key = self._config.get("api_key", "")
                if not api_key:
                    self.error.emit(tr("transcriber.error.no_api_key"))
                    return
                client = mistral_class()(api_key=api_key)

            # Chunk every audio file up front so progress covers the whole batch.
            per_file_chunks = [
                [] if is_transcript_file(path) else AudioChunker.chunk_audio(path, max_minutes) for path in paths
            ]
            total = sum(len(chunks) for chunks in per_file_chunks)
            file_count = len(paths)
            full_text_parts = []
            done = 0

            log.info("Transcription batch: %d file(s), %d audio chunk(s)", file_count, total)

            for file_index, (path, chunks) in enumerate(zip(paths, per_file_chunks)):
                log.info(
                    "File %d/%d: %s (%d chunk(s))", file_index + 1, file_count, os.path.basename(path), len(chunks)
                )
                if file_count > 1:
                    self.file_started.emit(file_index + 1, file_count, os.path.basename(path))

                if is_transcript_file(path):
                    # Already transcribed by someone else — take it verbatim, and in
                    # particular do not run the STT artifact cleanup over it.
                    text = read_transcript_file(path).strip()
                    log.info("  read existing transcript, %d chars", len(text))
                    full_text_parts.append(text)
                    # No chunk_completed here: an imported transcript can be hundreds of
                    # KB, and completed() sets the full text in the display anyway, so
                    # appending it first would only build the same document twice.
                    continue

                file_parts = []
                for chunk_path in chunks:
                    done += 1
                    self.progress.emit(done, total)
                    text = _transcribe_file(client, chunk_path, self._config)
                    log.info("  chunk %d/%d transcribed, %d chars", done, total, len(text))
                    file_parts.append(text)
                    self.chunk_completed.emit(done - 1, text)
                full_text_parts.append(_strip_stt_artifacts("\n\n".join(file_parts)))
                log.info("  artifact cleanup done for %s", os.path.basename(path))

            full_text = "\n\n".join(part for part in full_text_parts if part.strip())

            # Save transcript next to the first input file (all files share a session dir)
            session_dir = os.path.dirname(paths[0])
            transcript_path = os.path.join(session_dir, "transcript.txt")
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(full_text)

            log.info("Transcript written to %s (%d chars)", transcript_path, len(full_text))
            self.completed.emit(full_text)

        except Exception as e:
            log.exception("Transcription failed")
            self.error.emit(tr("transcriber.error.transcription", error=e))

        finally:
            # Release the connection pool and event loop instead of leaving them
            # to the garbage collector, which tears them down in bursts.
            if client is not None:
                client.__exit__(None, None, None)


class LiveTranscriptionWorker(QObject):
    """Transcribes a single audio chunk for live/incremental transcription."""

    completed = Signal(str)  # transcribed text
    error = Signal(str)

    def __init__(self, source, config: dict):
        """Initialize the worker.

        Args:
            source: Either the path of an existing FLAC chunk, or a
                ``(blocks, samplerate, flac_path)`` triple handed over by
                :meth:`AudioRecorder.take_pending_audio`, in which case the FLAC is
                encoded here rather than on the GUI thread.
            config: Campaign configuration dict.
        """
        super().__init__()
        self._source = source
        self._config = config

    def _encode_source(self) -> str:
        """Return the FLAC path to upload, encoding the pending buffer if needed."""
        if isinstance(self._source, str):
            return self._source
        blocks, samplerate, flac_path = self._source
        sf.write(flac_path, np.concatenate(blocks), samplerate, format="FLAC")
        return flac_path

    def run(self):
        """Transcribe a single audio chunk and emit the result."""
        flac_path = None
        try:
            mistral_cls = mistral_class()
            api_key = self._config.get("api_key", "")
            if not api_key:
                self.error.emit(tr("transcriber.error.no_api_key_short"))
                return

            flac_path = self._encode_source()
            # Closing the client releases its connection pool and event loop. Left to
            # the garbage collector they pile up and are torn down in bursts instead.
            with mistral_cls(api_key=api_key) as client:
                text = _transcribe_file(client, flac_path, self._config)
            text = _strip_stt_artifacts(text)

            self.completed.emit(text)

        except Exception as e:
            self.error.emit(tr("transcriber.error.live_transcription", error=e))

        finally:
            # Clean up the temp FLAC chunk whether or not the upload succeeded
            if flac_path:
                try:
                    os.remove(flac_path)
                except OSError:
                    pass


def start_transcription(wav_paths, config: dict) -> tuple[QThread, TranscriptionWorker]:
    """Create a transcription worker in a new thread.

    Args:
        wav_paths: A single path, or an ordered list of audio and/or transcript paths.
        config: Campaign configuration dict.

    Returns:
        The (thread, worker) pair; the caller starts the thread.
    """
    thread = QThread()
    worker = TranscriptionWorker(wav_paths, config)
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.completed.connect(thread.quit)
    worker.error.connect(thread.quit)
    return thread, worker


def start_live_transcription(source, config: dict) -> tuple[QThread, LiveTranscriptionWorker]:
    """Create a live transcription worker in a new thread.

    Args:
        source: A FLAC path, or the triple returned by ``take_pending_audio()``.
        config: Campaign configuration dict.

    Returns:
        The (thread, worker) pair; the caller starts the thread.
    """
    thread = QThread()
    worker = LiveTranscriptionWorker(source, config)
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.completed.connect(thread.quit)
    worker.error.connect(thread.quit)
    return thread, worker
