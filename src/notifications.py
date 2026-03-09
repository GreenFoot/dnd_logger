"""Notification sounds and taskbar flash for completion events."""

import ctypes
import logging
import os

from PySide6.QtCore import QUrl

from .utils import resource_path

log = logging.getLogger(__name__)


class NotificationSounds:
    """Manages notification sound effects using lazy-loaded QSoundEffect.

    Sounds are only initialized on first play() to avoid interfering
    with PortAudio (sounddevice) during recording/transcription.
    """

    _NAMES = ("transcription_done", "summary_done", "error")

    def __init__(self):
        self._sounds = {}
        self._loaded = False

    def _ensure_loaded(self):
        """Lazily create QSoundEffect instances on first use."""
        if self._loaded:
            return
        self._loaded = True

        from PySide6.QtMultimedia import (  # noqa: E501  # late import to avoid early audio init
            QSoundEffect,
        )

        for name in self._NAMES:
            path = resource_path(f"assets/sounds/{name}.wav")
            if os.path.exists(path):
                effect = QSoundEffect()
                effect.setSource(QUrl.fromLocalFile(path))
                effect.setVolume(0.5)
                self._sounds[name] = effect
            else:
                log.warning("Notification sound not found: %s", path)

    def play(self, name: str):
        """Play a named notification sound, loading on first call."""
        self._ensure_loaded()
        if name in self._sounds:
            effect = self._sounds[name]
            if effect.isPlaying():
                effect.stop()
            effect.play()


# Windows FLASHWINFO structure for taskbar flashing
class _FLASHWINFO(ctypes.Structure):  # pylint: disable=invalid-name
    """Win32 FLASHWINFO structure."""

    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("hwnd", ctypes.c_void_p),
        ("dwFlags", ctypes.c_uint),
        ("uCount", ctypes.c_uint),
        ("dwTimeout", ctypes.c_uint),
    ]


def flash_taskbar(hwnd: int, count: int = 3):
    """Flash the taskbar button to attract attention (Windows only)."""
    try:
        flashw_all = 0x03
        flashw_timernofg = 0x0C

        fwi = _FLASHWINFO(
            cbSize=ctypes.sizeof(_FLASHWINFO),
            hwnd=hwnd,
            dwFlags=flashw_all | flashw_timernofg,
            uCount=count,
            dwTimeout=0,
        )
        ctypes.windll.user32.FlashWindowEx(ctypes.byref(fwi))
    except Exception:
        log.debug("Taskbar flash failed", exc_info=True)
