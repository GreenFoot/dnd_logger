"""Gold corner bracket overlay — minimal L-shaped decorations."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget


class GoldFiligreeOverlay(QWidget):
    """Draws minimal gold L-bracket lines at the four corners of its parent.

    Each bracket is two thin lines (one horizontal, one vertical) meeting
    at the corner — like elegant photo mounting corners. ~15px per side.
    Mouse-transparent, zero ongoing CPU cost.
    """

    def __init__(self, parent=None, corner_size=15):
        super().__init__(parent)
        self._arm = corner_size

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        if parent:
            parent.installEventFilter(self)
            self.raise_()

    def eventFilter(self, obj, event):
        from PyQt6.QtCore import QEvent
        if obj is self.parent() and event.type() == QEvent.Type.Resize:
            self.setGeometry(self.parent().rect())
            self.raise_()
        return False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        arm = self._arm
        inset = 4  # px from actual edge

        gold = QColor(201, 168, 50, 100)
        pen = QPen(gold, 1.0)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        # Top-left
        painter.drawLine(inset, inset, inset + arm, inset)
        painter.drawLine(inset, inset, inset, inset + arm)

        # Top-right
        painter.drawLine(w - inset, inset, w - inset - arm, inset)
        painter.drawLine(w - inset, inset, w - inset, inset + arm)

        # Bottom-left
        painter.drawLine(inset, h - inset, inset + arm, h - inset)
        painter.drawLine(inset, h - inset, inset, h - inset - arm)

        # Bottom-right
        painter.drawLine(w - inset, h - inset, w - inset - arm, h - inset)
        painter.drawLine(w - inset, h - inset, w - inset, h - inset - arm)

        painter.end()

    def showEvent(self, event):
        super().showEvent(event)
        if self.parent():
            self.setGeometry(self.parent().rect())
            self.raise_()
