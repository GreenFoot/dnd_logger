"""Campaign-themed particle overlays and aurora shimmer for recording mode.

Supports 6 distinct particle types mapped to D&D campaigns:
  snow     — Icewind Dale, Storm King's Thunder
  embers   — Descent into Avernus
  mist     — Curse of Strahd
  spores   — Tomb of Annihilation
  dust     — Waterdeep: Dragon Heist
  faerzress — Out of the Abyss
"""

import math
import random

from PySide6.QtCore import QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPen, QRadialGradient
from PySide6.QtWidgets import QWidget

# ── Base particle ─────────────────────────────────────────


class BaseParticle:
    """Abstract particle with position, size, opacity, and fade-in logic."""

    __slots__ = ("x", "y", "size", "speed", "opacity", "fade_in", "active", "_extra")

    def __init__(self):
        """Initialize base particle attributes to defaults."""
        self.x = 0.0
        self.y = 0.0
        self.size = 0.0
        self.speed = 0.0
        self.opacity = 0.0
        self.fade_in = True
        self.active = False

    def reset(self, width, height, start_top=True):
        """Reinitialize to a random starting state."""
        raise NotImplementedError

    def update(self, dt, width, height):
        """Advance the particle by *dt* seconds."""
        raise NotImplementedError

    def draw(self, painter: QPainter, color_rgb: tuple):
        """Draw this particle using *painter* with the given base (R,G,B)."""
        raise NotImplementedError

    # shared fade-in helper
    def _do_fade_in(self, dt, rate=2.0):
        if self.fade_in:
            self.opacity = min(1.0, self.opacity + dt * rate)
            if self.opacity >= 1.0:
                self.fade_in = False


# ── Snow (Icewind Dale / Storm King) ─────────────────────


class SnowParticle(BaseParticle):
    __slots__ = ("x", "y", "size", "speed", "opacity", "fade_in", "active", "drift_phase", "drift_amp")

    def __init__(self, width, height):
        super().__init__()
        self.drift_phase = 0.0
        self.drift_amp = 0.0
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
        self.y += self.speed * dt * 30
        self.drift_phase += dt * 1.5
        self.x += math.sin(self.drift_phase) * self.drift_amp * dt * 15
        self._do_fade_in(dt)
        if not self.fade_in and self.y > height - 40:
            self.opacity = max(0.0, self.opacity - dt * 3)
        if self.y > height + 10 or (self.opacity <= 0 and not self.fade_in):
            self.reset(width, height)

    def draw(self, painter: QPainter, color_rgb: tuple):
        if self.opacity <= 0:
            return
        r, g, b = color_rgb
        color = QColor(r, g, b, int(self.opacity * 100))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(color)

        if self.size > 4:
            cx, cy = self.x, self.y
            hs = self.size / 2
            pen = QPen(color, 1.0)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawLine(QRectF(cx - hs, cy, cx + hs, cy).topLeft(), QRectF(cx - hs, cy, cx + hs, cy).bottomRight())
            painter.drawLine(QRectF(cx, cy - hs, cx, cy + hs).topLeft(), QRectF(cx, cy - hs, cx, cy + hs).bottomRight())
            painter.setPen(Qt.PenStyle.NoPen)
            core = QColor(255, 255, 255, int(self.opacity * 140))
            painter.setBrush(core)
            cs = self.size * 0.25
            painter.drawEllipse(QRectF(cx - cs / 2, cy - cs / 2, cs, cs))
        else:
            painter.drawEllipse(QRectF(self.x - self.size / 2, self.y - self.size / 2, self.size, self.size))
            if self.size > 3:
                core = QColor(255, 255, 255, int(self.opacity * 140))
                painter.setBrush(core)
                cs = self.size * 0.3
                painter.drawEllipse(QRectF(self.x - cs / 2, self.y - cs / 2, cs, cs))


# ── Embers (Descent into Avernus) ────────────────────────


class EmberParticle(BaseParticle):
    __slots__ = ("x", "y", "size", "speed", "opacity", "fade_in", "active", "wobble_phase", "wobble_amp", "glow_size")

    def __init__(self, width, height):
        super().__init__()
        self.wobble_phase = 0.0
        self.wobble_amp = 0.0
        self.glow_size = 0.0
        self.reset(width, height, start_top=False)

    def reset(self, width, height, start_top=True):
        self.x = random.uniform(0, width)
        self.y = height + random.uniform(0, 20) if start_top else random.uniform(0, height)
        self.size = random.uniform(2, 4)
        self.speed = random.uniform(0.3, 0.8)
        self.wobble_phase = random.uniform(0, math.pi * 2)
        self.wobble_amp = random.uniform(0.3, 0.7)
        self.glow_size = self.size * random.uniform(2.5, 4.0)
        self.opacity = 0.0
        self.fade_in = True
        self.active = True

    def update(self, dt, width, height):
        # Rise upward
        self.y -= self.speed * dt * 30
        self.wobble_phase += dt * 2.0
        self.x += math.sin(self.wobble_phase) * self.wobble_amp * dt * 10
        self._do_fade_in(dt, rate=1.5)
        if not self.fade_in and self.y < 40:
            self.opacity = max(0.0, self.opacity - dt * 2)
        if self.y < -10 or (self.opacity <= 0 and not self.fade_in):
            self.reset(width, height)

    def draw(self, painter: QPainter, color_rgb: tuple):
        if self.opacity <= 0:
            return
        r, g, b = color_rgb
        # Outer glow via radial gradient
        grad = QRadialGradient(self.x, self.y, self.glow_size)
        grad.setColorAt(0, QColor(r, g, b, int(self.opacity * 80)))
        grad.setColorAt(0.4, QColor(r, g, b, int(self.opacity * 40)))
        grad.setColorAt(1, QColor(r, g, b, 0))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(grad)
        gs = self.glow_size
        painter.drawEllipse(QRectF(self.x - gs, self.y - gs, gs * 2, gs * 2))

        # Bright core
        core = QColor(255, min(255, g + 80), min(255, b + 40), int(self.opacity * 160))
        painter.setBrush(core)
        hs = self.size / 2
        painter.drawEllipse(QRectF(self.x - hs, self.y - hs, self.size, self.size))


# ── Mist (Curse of Strahd) ───────────────────────────────


class MistParticle(BaseParticle):
    __slots__ = ("x", "y", "size", "speed", "opacity", "fade_in", "active", "drift_dir", "pulse_phase", "max_opacity")

    def __init__(self, width, height):
        super().__init__()
        self.drift_dir = 0.0
        self.pulse_phase = 0.0
        self.max_opacity = 0.0
        self.reset(width, height, start_top=False)

    def reset(self, width, height, start_top=True):
        self.x = random.uniform(-40, width + 40)
        self.y = random.uniform(height * 0.3, height * 0.9)
        self.size = random.uniform(60, 120)
        self.speed = random.uniform(0.05, 0.15)
        self.drift_dir = random.choice([-1, 1])
        self.pulse_phase = random.uniform(0, math.pi * 2)
        self.max_opacity = random.uniform(0.15, 0.30)
        self.opacity = 0.0
        self.fade_in = True
        self.active = True

    def update(self, dt, width, height):
        self.x += self.drift_dir * self.speed * dt * 20
        self.y += math.sin(self.pulse_phase) * 0.1 * dt * 10
        self.pulse_phase += dt * 0.4
        self._do_fade_in(dt, rate=0.3)
        # Soft pulsing opacity
        if not self.fade_in:
            pulse = (math.sin(self.pulse_phase) + 1) / 2
            self.opacity = self.max_opacity * (0.6 + 0.4 * pulse)
        # Wrap around
        if self.x > width + self.size:
            self.x = -self.size
        elif self.x < -self.size:
            self.x = width + self.size

    def draw(self, painter: QPainter, color_rgb: tuple):
        if self.opacity <= 0:
            return
        r, g, b = color_rgb
        alpha = int(self.opacity * 255)
        grad = QRadialGradient(self.x, self.y, self.size / 2)
        grad.setColorAt(0, QColor(r, g, b, alpha))
        grad.setColorAt(0.5, QColor(r, g, b, alpha // 2))
        grad.setColorAt(1, QColor(r, g, b, 0))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(grad)
        hs = self.size / 2
        # Ellipse wider than tall for misty look
        painter.drawEllipse(QRectF(self.x - hs * 1.5, self.y - hs * 0.6, self.size * 1.5, self.size * 0.6))


# ── Spores (Tomb of Annihilation) ────────────────────────


class SporeParticle(BaseParticle):
    __slots__ = ("x", "y", "size", "speed", "opacity", "fade_in", "active", "dx", "dy", "pulse_phase", "brightness")

    def __init__(self, width, height):
        super().__init__()
        self.dx = 0.0
        self.dy = 0.0
        self.pulse_phase = 0.0
        self.brightness = 0.0
        self.reset(width, height, start_top=False)

    def reset(self, width, height, start_top=True):
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.size = random.uniform(1.5, 3.0)
        self.speed = random.uniform(0.1, 0.3)
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)
        self.pulse_phase = random.uniform(0, math.pi * 2)
        self.brightness = 0.0
        self.opacity = 0.0
        self.fade_in = True
        self.active = True

    def update(self, dt, width, height):
        # Brownian motion: random direction changes
        self.dx += random.gauss(0, 1.5) * dt
        self.dy += random.gauss(0, 1.5) * dt
        # Clamp drift speed
        max_speed = 1.0
        self.dx = max(-max_speed, min(max_speed, self.dx))
        self.dy = max(-max_speed, min(max_speed, self.dy))
        self.x += self.dx * self.speed * dt * 30
        self.y += self.dy * self.speed * dt * 30
        self._do_fade_in(dt, rate=1.0)
        # Occasional brightness pulse
        self.pulse_phase += dt * 2.0
        self.brightness = max(0, math.sin(self.pulse_phase)) ** 4
        # Wrap around
        if self.x < -5:
            self.x = width + 5
        elif self.x > width + 5:
            self.x = -5
        if self.y < -5:
            self.y = height + 5
        elif self.y > height + 5:
            self.y = -5

    def draw(self, painter: QPainter, color_rgb: tuple):
        if self.opacity <= 0:
            return
        r, g, b = color_rgb
        # Mix in brightness pulse
        br = self.brightness
        alpha = int(self.opacity * (60 + 100 * br))
        cr = min(255, int(r + (255 - r) * br * 0.5))
        cg = min(255, int(g + (255 - g) * br * 0.5))
        cb = min(255, int(b + (255 - b) * br * 0.5))
        color = QColor(cr, cg, cb, alpha)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        hs = self.size / 2
        painter.drawEllipse(QRectF(self.x - hs, self.y - hs, self.size, self.size))


# ── Dust (Waterdeep: Dragon Heist) ───────────────────────


class DustParticle(BaseParticle):
    __slots__ = ("x", "y", "size", "speed", "opacity", "fade_in", "active", "drift_phase")

    def __init__(self, width, height):
        super().__init__()
        self.drift_phase = 0.0
        self.reset(width, height, start_top=False)

    def reset(self, width, height, start_top=True):
        self.x = random.uniform(0, width)
        self.y = random.uniform(-10, 0) if start_top else random.uniform(0, height)
        self.size = random.uniform(1.0, 2.5)
        self.speed = random.uniform(0.08, 0.2)
        self.drift_phase = random.uniform(0, math.pi * 2)
        self.opacity = 0.0
        self.fade_in = True
        self.active = True

    def update(self, dt, width, height):
        self.y += self.speed * dt * 20
        self.drift_phase += dt * 0.8
        self.x += math.sin(self.drift_phase) * 0.15 * dt * 10
        self._do_fade_in(dt, rate=1.0)
        if not self.fade_in and self.y > height - 30:
            self.opacity = max(0.0, self.opacity - dt * 2)
        if self.y > height + 5 or (self.opacity <= 0 and not self.fade_in):
            self.reset(width, height)

    def draw(self, painter: QPainter, color_rgb: tuple):
        if self.opacity <= 0:
            return
        r, g, b = color_rgb
        color = QColor(r, g, b, int(self.opacity * 50))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        hs = self.size / 2
        painter.drawEllipse(QRectF(self.x - hs, self.y - hs, self.size, self.size))


# ── Faerzress (Out of the Abyss) ─────────────────────────


class FaerzressParticle(BaseParticle):
    __slots__ = (
        "x",
        "y",
        "size",
        "speed",
        "opacity",
        "fade_in",
        "active",
        "pulse_phase",
        "pulse_speed",
        "glow_radius",
        "base_opacity",
    )

    def __init__(self, width, height):
        super().__init__()
        self.pulse_phase = 0.0
        self.pulse_speed = 0.0
        self.glow_radius = 0.0
        self.base_opacity = 0.0
        self.reset(width, height, start_top=False)

    def reset(self, width, height, start_top=True):
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.size = random.uniform(3, 6)
        self.speed = random.uniform(0.01, 0.04)  # near-stationary
        self.pulse_phase = random.uniform(0, math.pi * 2)
        self.pulse_speed = random.uniform(0.5, 1.2)
        self.glow_radius = self.size * random.uniform(3, 6)
        self.base_opacity = random.uniform(0.3, 0.6)
        self.opacity = 0.0
        self.fade_in = True
        self.active = True

    def update(self, dt, width, height):
        # Near-stationary with very slow drift
        self.x += random.gauss(0, 0.3) * dt * 5
        self.y += random.gauss(0, 0.3) * dt * 5
        self.pulse_phase += dt * self.pulse_speed
        self._do_fade_in(dt, rate=0.5)
        # Breathing opacity
        if not self.fade_in:
            breath = (math.sin(self.pulse_phase) + 1) / 2
            self.opacity = self.base_opacity * (0.3 + 0.7 * breath)
        # Soft bounds (wrap)
        if self.x < -self.glow_radius:
            self.x = width + self.glow_radius
        elif self.x > width + self.glow_radius:
            self.x = -self.glow_radius
        if self.y < -self.glow_radius:
            self.y = height + self.glow_radius
        elif self.y > height + self.glow_radius:
            self.y = -self.glow_radius

    def draw(self, painter: QPainter, color_rgb: tuple):
        if self.opacity <= 0:
            return
        r, g, b = color_rgb
        alpha = int(self.opacity * 255)
        grad = QRadialGradient(self.x, self.y, self.glow_radius)
        grad.setColorAt(0, QColor(r, g, b, alpha))
        grad.setColorAt(0.3, QColor(r, g, b, alpha // 2))
        grad.setColorAt(0.7, QColor(r, g, b, alpha // 5))
        grad.setColorAt(1, QColor(r, g, b, 0))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(grad)
        gr = self.glow_radius
        painter.drawEllipse(QRectF(self.x - gr, self.y - gr, gr * 2, gr * 2))

        # Bright inner core
        core_alpha = int(self.opacity * 180)
        core = QColor(min(255, r + 60), min(255, g + 60), min(255, b + 60), core_alpha)
        painter.setBrush(core)
        hs = self.size / 2
        painter.drawEllipse(QRectF(self.x - hs, self.y - hs, self.size, self.size))


# ── Particle type registry ────────────────────────────────

PARTICLE_TYPES = {
    "snow": (SnowParticle, 12),
    "embers": (EmberParticle, 10),
    "mist": (MistParticle, 5),
    "spores": (SporeParticle, 18),
    "dust": (DustParticle, 15),
    "faerzress": (FaerzressParticle, 8),
}

DEFAULT_PARTICLE_TYPE = "snow"


# ── Overlay widget ────────────────────────────────────────


class SnowParticleOverlay(QWidget):
    """Lightweight overlay that renders themed particles across the parent widget.

    Starts/stops with recording. Particle type determines physics + rendering.
    """

    def __init__(self, parent=None, num_particles=12, particle_color=None, particle_type=None):
        super().__init__(parent)
        self._particle_type = particle_type or DEFAULT_PARTICLE_TYPE
        self._particle_class, default_count = PARTICLE_TYPES.get(
            self._particle_type, PARTICLE_TYPES[DEFAULT_PARTICLE_TYPE]
        )
        self._num_particles = num_particles if num_particles != 12 else default_count
        self._particles = []
        self._running = False
        self._particle_color = tuple(particle_color) if particle_color else (220, 240, 255)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        self._timer = QTimer(self)
        self._timer.setInterval(50)  # ~20fps
        self._timer.timeout.connect(self._tick)

        if parent:
            parent.installEventFilter(self)

    def set_particle_type(self, ptype: str):
        """Switch to a different particle type. Restarts if currently running."""
        if ptype not in PARTICLE_TYPES:
            ptype = DEFAULT_PARTICLE_TYPE
        if ptype == self._particle_type:
            return
        was_running = self._running
        if was_running:
            self.stop()
        self._particle_type = ptype
        self._particle_class, self._num_particles = PARTICLE_TYPES[ptype]
        if was_running:
            self.start()

    def start(self):
        """Spawn particles and begin the animation timer."""
        if self._running:
            return
        self._running = True
        w, h = self.width() or 400, self.height() or 600
        self._particles = [self._particle_class(w, h) for _ in range(self._num_particles)]
        self._timer.start()
        self.show()
        self.raise_()

    def stop(self):
        """Stop the animation and clear all particles."""
        self._running = False
        self._timer.stop()
        self._particles.clear()
        self.update()

    def set_particle_color(self, rgb: tuple):
        """Update the particle color (R, G, B)."""
        self._particle_color = tuple(rgb)

    def eventFilter(self, obj, event):
        """Resize overlay to match parent on parent resize events."""
        from PySide6.QtCore import QEvent

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
        """Draw all active particles onto the overlay."""
        if not self._particles:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = self._particle_color
        for p in self._particles:
            p.draw(painter, color)
        painter.end()

    def showEvent(self, event):
        """Sync overlay geometry to parent when shown."""
        super().showEvent(event)
        if self.parent():
            self.setGeometry(self.parent().rect())
            self.raise_()


# ── Aurora shimmer (unchanged) ────────────────────────────


class AuroraShimmerOverlay(QWidget):
    """Subtle background color shimmer during recording.

    Cycles through deep aurora tones (dark teal -> dark purple -> dark blue)
    over ~10s. Barely perceptible — atmospheric only.
    """

    def __init__(self, parent=None, aurora_tones=None):
        super().__init__(parent)
        self._phase = 0.0
        self._running = False
        self._aurora_tones = aurora_tones or [[10, 25, 35], [20, 15, 45], [15, 20, 35]]

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        self._timer = QTimer(self)
        self._timer.setInterval(100)  # 10fps
        self._timer.timeout.connect(self._tick)

        if parent:
            parent.installEventFilter(self)

    def start(self):
        """Begin the aurora color-cycling animation."""
        if self._running:
            return
        self._running = True
        self._phase = 0.0
        self._timer.start()
        self.show()
        self.raise_()

    def stop(self):
        """Stop the aurora animation and hide the overlay."""
        self._running = False
        self._timer.stop()
        self.hide()

    def set_aurora_tones(self, tones: list):
        """Update the aurora tones — list of 3 [R,G,B] values."""
        self._aurora_tones = tones

    def eventFilter(self, obj, event):
        """Resize overlay to match parent on parent resize events."""
        from PySide6.QtCore import QEvent

        if obj is self.parent() and event.type() == QEvent.Type.Resize:
            self.setGeometry(self.parent().rect())
        return False

    def _tick(self):
        self._phase += 0.1 * 0.05  # very slow: full cycle ~10s
        if self._phase > 1.0:
            self._phase -= 1.0
        self.update()

    def paintEvent(self, event):
        """Render the radial aurora gradient across the overlay."""
        if not self._running:
            return

        painter = QPainter(self)
        w = self.width()
        h = self.height()

        t0, t1, t2 = self._aurora_tones

        # Cycle through aurora colors
        p = self._phase
        if p < 0.333:
            t = p / 0.333
            r = int(t0[0] + t * (t1[0] - t0[0]))
            g = int(t0[1] + t * (t1[1] - t0[1]))
            b = int(t0[2] + t * (t1[2] - t0[2]))
        elif p < 0.666:
            t = (p - 0.333) / 0.333
            r = int(t1[0] + t * (t2[0] - t1[0]))
            g = int(t1[1] + t * (t2[1] - t1[1]))
            b = int(t1[2] + t * (t2[2] - t1[2]))
        else:
            t = (p - 0.666) / 0.334
            r = int(t2[0] + t * (t0[0] - t2[0]))
            g = int(t2[1] + t * (t0[1] - t2[1]))
            b = int(t2[2] + t * (t0[2] - t2[2]))

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
        """Sync overlay geometry to parent when shown."""
        super().showEvent(event)
        if self.parent():
            self.setGeometry(self.parent().rect())
