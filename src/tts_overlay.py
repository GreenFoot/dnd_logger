"""TTSOverlay — animated overlay shown during text-to-speech playback."""

import math

from PySide6.QtCore import QEvent, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QWidget


class TTSOverlay(QWidget):
    """Semi-transparent overlay with sound-wave animation and TTS control hints.

    Signals:
        pause_toggled: emitted when the user presses Space.
        stop_requested: emitted when the user presses Escape.
    """

    pause_toggled = Signal()
    stop_requested = Signal()

    _BAR_COUNT = 7
    _BAR_WIDTH = 8
    _BAR_GAP = 5
    _BAR_MAX_H = 36
    _BAR_MIN_H = 6

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._paused = False
        self._tick = 0
        self._bar_heights = [self._BAR_MIN_H] * self._BAR_COUNT
        self._prev_focus = None

        self._anim_timer = QTimer(self)
        self._anim_timer.setInterval(50)
        self._anim_timer.timeout.connect(self._animate)

        if parent:
            parent.installEventFilter(self)

        self.hide()

    # ── Public slots ──────────────────────────────────

    def show_overlay(self):
        """Show overlay and start animation."""
        if not self.isVisible():
            from PySide6.QtWidgets import QApplication
            self._prev_focus = QApplication.focusWidget()
        self._paused = False
        self._tick = 0
        self._sync_geometry()
        self.raise_()
        self.show()
        self.setFocus()
        self._anim_timer.start()

    def hide_overlay(self):
        """Hide overlay and stop animation."""
        self._anim_timer.stop()
        self.hide()
        if self._prev_focus and not self._prev_focus.isHidden():
            self._prev_focus.setFocus()
        self._prev_focus = None

    def set_paused(self, paused: bool):
        """Update visual state for paused / playing."""
        self._paused = paused
        if paused:
            self._anim_timer.stop()
        else:
            self._anim_timer.start()
        self.update()

    # ── Event handling ────────────────────────────────

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.pause_toggled.emit()
        elif event.key() == Qt.Key.Key_Escape:
            self.stop_requested.emit()
        else:
            super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        if obj == self.parentWidget() and event.type() == QEvent.Type.Resize:
            if self.isVisible():
                self._sync_geometry()
        return False

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()

        # Full-area dim
        p.fillRect(0, 0, w, h, QColor(13, 13, 30, 160))

        # Centred card
        card_w, card_h = 300, 160
        cx = (w - card_w) / 2
        cy = (h - card_h) / 2

        card = QPainterPath()
        card.addRoundedRect(QRectF(cx, cy, card_w, card_h), 14, 14)
        p.fillPath(card, QColor(25, 20, 35, 235))
        p.setPen(QPen(QColor(212, 175, 55, 100), 1.5))
        p.drawPath(card)

        # Sound-wave bars
        total_bw = (self._BAR_COUNT * self._BAR_WIDTH
                     + (self._BAR_COUNT - 1) * self._BAR_GAP)
        bx_start = (w - total_bw) / 2
        bars_cy = cy + 55

        bar_color = QColor(126, 200, 227) if self._paused else QColor(212, 175, 55)

        for i in range(self._BAR_COUNT):
            bh = self._bar_heights[i]
            bx = bx_start + i * (self._BAR_WIDTH + self._BAR_GAP)
            by = bars_cy - bh / 2
            bar = QPainterPath()
            bar.addRoundedRect(QRectF(bx, by, self._BAR_WIDTH, bh), 3, 3)
            p.fillPath(bar, bar_color)

        # Status label
        p.setPen(QColor(230, 220, 200))
        sf = QFont("Cinzel", 11)
        sf.setBold(True)
        p.setFont(sf)
        label = "En pause" if self._paused else "Lecture en cours\u2026"
        p.drawText(QRectF(cx, cy + 85, card_w, 24),
                   Qt.AlignmentFlag.AlignCenter, label)

        # Control hints
        p.setPen(QColor(160, 155, 145))
        hf = QFont("Segoe UI", 9)
        p.setFont(hf)
        pause_hint = "Espace : Reprendre" if self._paused else "Espace : Pause"
        hints = f"{pause_hint}  |  \u00c9chap : Arr\u00eater"
        p.drawText(QRectF(cx, cy + 118, card_w, 20),
                   Qt.AlignmentFlag.AlignCenter, hints)

        p.end()

    # ── Private ───────────────────────────────────────

    def _sync_geometry(self):
        parent = self.parentWidget()
        if parent:
            self.setGeometry(0, 0, parent.width(), parent.height())

    def _animate(self):
        self._tick += 1
        for i in range(self._BAR_COUNT):
            phase = i * 0.9
            self._bar_heights[i] = self._BAR_MIN_H + (
                self._BAR_MAX_H - self._BAR_MIN_H
            ) * (0.5 + 0.5 * math.sin(self._tick * 0.15 + phase))
        self.update()
