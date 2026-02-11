"""Audio recorder using sounddevice with streaming architecture."""

import os
import queue
import threading
from datetime import datetime

import numpy as np
import sounddevice as sd
import soundfile as sf
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

from .utils import ensure_dir, sessions_dir


class AudioRecorder(QObject):
    """Streams mic audio to a WAV file via a writer thread."""

    recording_started = pyqtSignal()
    recording_stopped = pyqtSignal(str)  # path to WAV
    level_update = pyqtSignal(float)  # 0.0-1.0 RMS level
    duration_update = pyqtSignal(int)  # seconds elapsed
    error_occurred = pyqtSignal(str)

    _SENTINEL = None  # signals writer thread to stop

    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self._config = config
        self._stream = None
        self._queue = queue.Queue()
        self._writer_thread = None
        self._wav_path = None
        self._is_recording = False
        self._elapsed = 0
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick)

    @property
    def is_recording(self) -> bool:
        return self._is_recording

    @property
    def wav_path(self) -> str | None:
        return self._wav_path

    def start_recording(self, device=None):
        """Start recording audio from the given device."""
        if self._is_recording:
            return
        try:
            sr = self._config.get("sample_rate", 16000)
            ch = self._config.get("channels", 1)

            # Create session folder
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_folder = os.path.join(sessions_dir(self._config), f"session_{ts}")
            ensure_dir(session_folder)
            self._wav_path = os.path.join(session_folder, "recording.wav")

            # Open soundfile for writing
            self._sf = sf.SoundFile(
                self._wav_path, mode="w", samplerate=sr, channels=ch, subtype="PCM_16"
            )

            # Clear queue
            while not self._queue.empty():
                try:
                    self._queue.get_nowait()
                except queue.Empty:
                    break

            # Start writer thread
            self._writer_thread = threading.Thread(
                target=self._writer_loop, daemon=True
            )
            self._writer_thread.start()

            # Determine device index
            dev_index = device
            if dev_index is None:
                dev_index = self._config.get("audio_device", None)

            # Start input stream
            self._stream = sd.InputStream(
                samplerate=sr,
                channels=ch,
                dtype="int16",
                device=dev_index,
                callback=self._audio_callback,
                blocksize=int(sr * 0.05),  # 50ms blocks
            )
            self._stream.start()
            self._is_recording = True
            self._elapsed = 0
            self._timer.start()
            self.recording_started.emit()

        except Exception as e:
            self.error_occurred.emit(f"Erreur d'enregistrement: {e}")
            self._cleanup_on_error()

    def stop_recording(self) -> str | None:
        """Stop recording and return path to WAV file."""
        if not self._is_recording:
            return None
        self._is_recording = False
        self._timer.stop()

        # Stop input stream
        if self._stream:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass
            self._stream = None

        # Signal writer thread to finish
        self._queue.put(self._SENTINEL)
        if self._writer_thread:
            self._writer_thread.join(timeout=5)
            self._writer_thread = None

        # Close soundfile
        if self._sf:
            try:
                self._sf.close()
            except Exception:
                pass
            self._sf = None

        path = self._wav_path
        self.recording_stopped.emit(path)
        return path

    def _audio_callback(self, indata, frames, time_info, status):
        """Called by PortAudio in its own thread — just enqueue data."""
        if status:
            pass  # Could log status flags
        self._queue.put(indata.copy())
        # Calculate RMS for VU meter
        rms = np.sqrt(np.mean(indata.astype(np.float32) ** 2)) / 32768.0
        self.level_update.emit(min(rms * 5, 1.0))  # Scale up for visibility

    def _writer_loop(self):
        """Writer thread: pulls data from queue and writes to disk."""
        while True:
            data = self._queue.get()
            if data is self._SENTINEL:
                break
            try:
                self._sf.write(data)
            except Exception:
                break

    def _tick(self):
        """Update duration counter every second."""
        self._elapsed += 1
        self.duration_update.emit(self._elapsed)

    def _cleanup_on_error(self):
        """Clean up resources after an error."""
        if self._stream:
            try:
                self._stream.close()
            except Exception:
                pass
            self._stream = None
        if hasattr(self, "_sf") and self._sf:
            try:
                self._sf.close()
            except Exception:
                pass
            self._sf = None
        self._is_recording = False

    @staticmethod
    def list_devices() -> list[dict]:
        """Return list of available input devices."""
        devices = []
        try:
            for i, dev in enumerate(sd.query_devices()):
                if dev["max_input_channels"] > 0:
                    devices.append({"index": i, "name": dev["name"],
                                    "channels": dev["max_input_channels"],
                                    "sample_rate": dev["default_samplerate"]})
        except Exception:
            pass
        return devices
