"""Tint the macOS window title bar with the active theme's background color.

Qt only draws inside the window content; the title bar belongs to the NSWindow.
Making the title bar transparent and setting the NSWindow background color makes
it blend with the themed content. No-op on other platforms.

Cocoa is called through the Objective-C runtime with ctypes rather than pyobjc:
importing pyobjc's AppKit in the same process as QtWebEngine crashes the app.
"""

import ctypes
import logging
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QGuiApplication, QWindow

log = logging.getLogger(__name__)

_objc = None
if sys.platform == "darwin":
    try:
        _objc = ctypes.cdll.LoadLibrary("/usr/lib/libobjc.dylib")
        _objc.objc_getClass.restype = ctypes.c_void_p
        _objc.objc_getClass.argtypes = [ctypes.c_char_p]
        _objc.sel_registerName.restype = ctypes.c_void_p
        _objc.sel_registerName.argtypes = [ctypes.c_char_p]
    except OSError:
        _objc = None

_color = None  # pylint: disable=invalid-name


def _msg(receiver, selector: str, *args, argtypes=(), restype=ctypes.c_void_p):
    """Send an Objective-C message with an explicit C signature (required on arm64).

    Args:
        receiver: The object or class pointer receiving the message.
        selector: The selector name, e.g. "setBackgroundColor:".
        *args: The message arguments.
        argtypes: The ctypes types of the arguments.
        restype: The ctypes return type.

    Returns:
        The message's return value.
    """
    send = ctypes.cast(_objc.objc_msgSend, ctypes.c_void_p).value
    func = ctypes.CFUNCTYPE(restype, ctypes.c_void_p, ctypes.c_void_p, *argtypes)(send)
    return func(receiver, _objc.sel_registerName(selector.encode()), *args)


def _cls(name: str) -> int:
    """Return the Objective-C class pointer for a class name."""
    return _objc.objc_getClass(name.encode())


def _is_titled_window(window: QWindow) -> bool:
    """Return whether the window is a visible top-level window with a title bar."""
    return window.isVisible() and window.type() in (Qt.WindowType.Window, Qt.WindowType.Dialog)


def _on_focus_window_changed(window: QWindow | None):
    """Tint windows as they get focus, which covers newly opened dialogs."""
    if window is not None and _is_titled_window(window):
        _tint(window, _color)


def _tint(window: QWindow, color: QColor):
    """Apply the color and a dark appearance to the window's NSWindow."""
    try:
        ns_window = _msg(int(window.winId()), "window")
        if not ns_window:
            return
        _msg(ns_window, "setTitlebarAppearsTransparent:", True, argtypes=(ctypes.c_bool,), restype=None)
        ns_color = _msg(
            _cls("NSColor"),
            "colorWithSRGBRed:green:blue:alpha:",
            color.redF(),
            color.greenF(),
            color.blueF(),
            1.0,
            argtypes=(ctypes.c_double,) * 4,
        )
        _msg(ns_window, "setBackgroundColor:", ns_color, argtypes=(ctypes.c_void_p,), restype=None)
        name = _msg(_cls("NSString"), "stringWithUTF8String:", b"NSAppearanceNameDarkAqua", argtypes=(ctypes.c_char_p,))
        appearance = _msg(_cls("NSAppearance"), "appearanceNamed:", name, argtypes=(ctypes.c_void_p,))
        _msg(ns_window, "setAppearance:", appearance, argtypes=(ctypes.c_void_p,), restype=None)
    except Exception:
        log.debug("Title bar tint failed", exc_info=True)


def set_title_bar_color(color: str | QColor):
    """Tint the title bar of all current and future windows with the given color.

    Args:
        color: A QColor or any color string QColor accepts (e.g. "#0a0f14").
    """
    global _color  # pylint: disable=global-statement
    if _objc is None:
        return
    if _color is None:
        QGuiApplication.instance().focusWindowChanged.connect(_on_focus_window_changed)
    _color = QColor(color)
    for window in QGuiApplication.topLevelWindows():
        if _is_titled_window(window):
            _tint(window, _color)
