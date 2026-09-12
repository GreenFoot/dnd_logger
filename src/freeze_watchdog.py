"""Detects and records GUI-thread freezes during long-running sessions.

A heartbeat QTimer on the GUI thread stamps the current time once a second. A
daemon thread watches that stamp; when it goes stale the GUI thread is wedged, so
it appends the stack of every thread to ``dnd_logger_stalls.log`` and, once the
heartbeat recovers, records how long the freeze lasted.

One dump is written per freeze episode rather than one per check, so arming this
for the whole of a three-hour recording costs nothing when nothing goes wrong.
"""

import faulthandler
import logging
import os
import threading
import time
from datetime import datetime

from PySide6.QtCore import QObject, QTimer

from .utils import project_root

log = logging.getLogger("dndlogger.freeze")

STALL_LOG = "dnd_logger_stalls.log"


class FreezeWatchdog(QObject):
    """Watches the GUI thread and dumps every thread's stack when it stops responding."""

    def __init__(self, parent=None, threshold: float = 5.0):
        """Initialize the watchdog.

        Args:
            parent: Parent QObject owning the heartbeat timer (must live on the GUI thread).
            threshold: Seconds the heartbeat may lag before a freeze is reported.
        """
        super().__init__(parent)
        self._threshold = threshold
        self._beat = time.monotonic()
        self._last_lag = 0.0
        self._label = ""
        self._stop = threading.Event()
        self._thread = None

        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._on_beat)

    def start(self, label: str = ""):
        """Begin watching the GUI thread.

        Args:
            label: Short description of the activity, written into the stall log.
        """
        if self._thread is not None:
            return
        self._label = label
        self._beat = time.monotonic()
        self._stop.clear()
        self._timer.start()
        self._thread = threading.Thread(target=self._watch, name="freeze-watchdog", daemon=True)
        self._thread.start()

    def stop(self):
        """Stop watching and join the watcher thread."""
        self._timer.stop()
        if self._thread is None:
            return
        self._stop.set()
        self._thread.join(timeout=3)
        self._thread = None

    def _on_beat(self):
        self._beat = time.monotonic()

    def _watch(self):
        """Poll the heartbeat from a daemon thread and report stalls."""
        reported = False
        while not self._stop.wait(1.0):
            lag = time.monotonic() - self._beat
            if lag > self._threshold and not reported:
                reported = True
                self._dump(lag)
            elif lag <= self._threshold and reported:
                reported = False
                self._append(f"----- GUI thread responsive again after ~{self._last_lag:.1f}s -----\n")
            if reported:
                self._last_lag = lag

    def _dump(self, lag: float):
        """Append a header and the stack of every thread to the stall log."""
        self._last_lag = lag
        header = (
            f"\n===== GUI thread frozen for {lag:.1f}s during '{self._label}' "
            f"at {datetime.now():%Y-%m-%d %H:%M:%S} =====\n"
        )
        try:
            with open(os.path.join(project_root(), STALL_LOG), "a", encoding="utf-8") as f:
                f.write(header)
                f.flush()
                faulthandler.dump_traceback(file=f, all_threads=True)
        except OSError:
            log.exception("Could not write the freeze dump")

    def _append(self, text: str):
        """Append a plain line to the stall log, ignoring I/O failures."""
        try:
            with open(os.path.join(project_root(), STALL_LOG), "a", encoding="utf-8") as f:
                f.write(text)
        except OSError:
            pass
