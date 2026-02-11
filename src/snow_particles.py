"""Snowflake particle overlay and aurora shimmer for recording mode."""

import math
import random

from PyQt6.QtCore import QRectF, Qt, QTimer
from PyQt6.QtGui import QColor, QPainter, QPen, QRadialGradient
from PyQt6.QtWidgets import QWidget


class Snowflake:
    """A single snowflake particle."""

    __slots__ = ("x", "y", "size", "speed", "drift_phase", "drift_amp",
                 "opacity", "fade_in", "active")

    def __init__(self, width, height):
        self.reset(width, height, start_top=False)

    def reset(self, width, height, start_top=True):
        self.x = random.uniform(0, width)
        self.y = random.uniform(-20, 0) if start_top else random.uniform(0, height)
        self.size = random.uniform(2, 6)
        self.speed = random.uniform(0.2, 0.7)
        self.drift_phase = random.uniform(0, math.pi * 2)
        self.drift_amp = random.uniform(0.2, 0.5)
        self.opacity = 0.0
        self.fade_in = True
        self.active = True

    def update(self, dt, width, height):
        """Advance particle by dt seconds."""
        self.y += self.speed * dt * 30
        self.drift_phase += dt * 1.5
        self.x += math.sin(self.drift_phase) * self.drift_amp * dt * 15

        # Fade in/out
        if self.fade_in:
            self.opacity = min(1.0, self.opacity + dt * 2)
            if self.opacity >= 1.0:
                self.fade_in = False
        elif self.y > height - 40:
            self.opacity = max(0.0, self.opacity - dt * 3)

        # Reset if off-screen or fully faded after crossing threshold
        if self.y > height + 10 or (self.opacity <= 0 and not self.fade_in):
            self.reset(width, height)


class SnowParticleOverlay(QWidget):
    """Lightweight overlay that drifts snowflakes across the parent widget.

    Starts/stops with recording. ~12 particles, 20fps.
    """

    def __init__(self, parent=None, num_particles=12):
        super().__init__(parent)
        self._num_particles = num_particles
        self._particles = []
        self._running = False

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        self._timer = QTimer(self)
        self._timer.setInterval(50)  # ~20fps
        self._timer.timeout.connect(self._tick)

        if parent:
            parent.installEventFilter(self)

    def start(self):
        if self._running:
            return
        self._running = True
        w, h = self.width() or 400, self.height() or 600
        self._particles = [Snowflake(w, h) for _ in range(self._num_particles)]
        self._timer.start()
        self.show()
        self.raise_()

    def stop(self):
        self._running = False
        self._timer.stop()
        self._particles.clear()
        self.update()

    def eventFilter(self, obj, event):
        from PyQt6.QtCore import QEvent
        if obj is self.parent() and event.type() == QEvent.Type.Resize:
            self.setGeometry(self.parent().rect())
            self.raise_()
        return False

    def _tick(self):
        w = self.width()
        h = self.height()
        dt = 0.05  # ~20fps
        for p in self._particles:
            p.update(dt, w, h)
        self.update()

    def paintEvent(self, event):
        if not self._particles:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for p in self._particles:
            if p.opacity <= 0:
                continue
            color = QColor(220, 240, 255, int(p.opacity * 100))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)

            if p.size > 4:
                # Star shape for larger flakes
                cx, cy = p.x, p.y
                hs = p.size / 2
                pen = QPen(color, 1.0)
                painter.setPen(pen)
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawLine(QRectF(cx - hs, cy, cx + hs, cy).topLeft(),
                                 QRectF(cx - hs, cy, cx + hs, cy).bottomRight())
                painter.drawLine(QRectF(cx, cy - hs, cx, cy + hs).topLeft(),
                                 QRectF(cx, cy - hs, cx, cy + hs).bottomRight())
                painter.setPen(Qt.PenStyle.NoPen)
                # Bright center dot
                core = QColor(255, 255, 255, int(p.opacity * 140))
                painter.setBrush(core)
                cs = p.size * 0.25
                painter.drawEllipse(QRectF(cx - cs / 2, cy - cs / 2, cs, cs))
            else:
                painter.drawEllipse(QRectF(p.x - p.size / 2, p.y - p.size / 2,
                                           p.size, p.size))
                # Tiny bright center
                if p.size > 3:
                    core = QColor(255, 255, 255, int(p.opacity * 140))
                    painter.setBrush(core)
                    cs = p.size * 0.3
                    painter.drawEllipse(QRectF(p.x - cs / 2, p.y - cs / 2, cs, cs))

        painter.end()

    def showEvent(self, event):
        super().showEvent(event)
        if self.parent():
            self.setGeometry(self.parent().rect())
            self.raise_()


class AuroraShimmerOverlay(QWidget):
    """Subtle background color shimmer during recording.

    Cycles through deep aurora tones (dark teal -> dark purple -> dark blue)
    over ~10s. Barely perceptible — atmospheric only.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._phase = 0.0
        self._running = False

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        self._timer = QTimer(self)
        self._timer.setInterval(100)  # 10fps
        self._timer.timeout.connect(self._tick)

        if parent:
            parent.installEventFilter(self)

    def start(self):
        if self._running:
            return
        self._running = True
        self._phase = 0.0
        self._timer.start()
        self.show()
        self.raise_()

    def stop(self):
        self._running = False
        self._timer.stop()
        self.hide()

    def eventFilter(self, obj, event):
        from PyQt6.QtCore import QEvent
        if obj is self.parent() and event.type() == QEvent.Type.Resize:
            self.setGeometry(self.parent().rect())
        return False

    def _tick(self):
        self._phase += 0.1 * 0.05  # very slow: full cycle ~10s
        if self._phase > 1.0:
            self._phase -= 1.0
        self.update()

    def paintEvent(self, event):
        if not self._running:
            return

        painter = QPainter(self)
        w = self.width()
        h = self.height()

        # Cycle through aurora colors
        p = self._phase
        if p < 0.333:
            t = p / 0.333
            r = int(10 + t * 10)
            g = int(25 - t * 10)
            b = int(35 + t * 10)
        elif p < 0.666:
            t = (p - 0.333) / 0.333
            r = int(20 - t * 5)
            g = int(15 + t * 5)
            b = int(45 - t * 10)
        else:
            t = (p - 0.666) / 0.334
            r = int(15 - t * 5)
            g = int(20 + t * 5)
            b = int(35)

        # Gradient origin: top-right with phase-based X oscillation
        x_origin = w * 0.7 + math.sin(p * math.pi * 2) * w * 0.1
        y_origin = -h * 0.1

        gradient = QRadialGradient(x_origin, y_origin, h * 0.8)
        gradient.setColorAt(0, QColor(r, g, b, 20))
        gradient.setColorAt(0.7, QColor(r, g, b, 8))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))

        painter.fillRect(0, 0, w, h, gradient)
        painter.end()

    def showEvent(self, event):
        super().showEvent(event)
        if self.parent():
            self.setGeometry(self.parent().rect())
