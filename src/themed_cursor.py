"""Themed cursors — gauntlet cursor loaded from PNG asset."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QPixmap

from .utils import resource_path

_GAUNTLET_PATH = "assets/images/cursors/gauntlet.png"
_CURSOR_SIZE = 32

# Hotspot as fraction of image size (fingertip position)
_HOTSPOT_X_FRAC = 0
_HOTSPOT_Y_FRAC = 0


def create_gauntlet_cursor() -> QCursor:
    """Load the gauntlet cursor from PNG, scale to cursor size.

    Returns:
        A QCursor with the gauntlet image and hotspot at the fingertip.
    """
    path = resource_path(_GAUNTLET_PATH)
    base = QPixmap(path)
    if base.isNull():
        return QCursor(Qt.CursorShape.ArrowCursor)

    scaled = base.scaled(
        _CURSOR_SIZE, _CURSOR_SIZE, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
    )

    hx = int(scaled.width() * _HOTSPOT_X_FRAC)
    hy = int(scaled.height() * _HOTSPOT_Y_FRAC)
    return QCursor(scaled, hx, hy)
