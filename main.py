"""DnD Logger — D&D Session Logger entry point."""

import ctypes
import os
import sys

# Set Windows App ID for proper taskbar icon grouping
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "dndlogger.dnd.sessionlogger.1"
    )
except Exception:
    pass

# PyInstaller: QWebEngine needs explicit paths to resources in frozen builds.
if hasattr(sys, "_MEIPASS"):
    _pyside_dir = os.path.join(sys._MEIPASS, "PySide6")
    os.environ["QTWEBENGINE_RESOURCES_PATH"] = os.path.join(_pyside_dir, "resources")
    os.environ["QTWEBENGINE_LOCALES_PATH"] = os.path.join(_pyside_dir, "translations", "qtwebengine_locales")
    os.environ["QTWEBENGINEPROCESS_PATH"] = os.path.join(_pyside_dir, "QtWebEngineProcess.exe")
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox"


def main():
    import traceback
    import logging
    from logging.handlers import RotatingFileHandler

    from src.utils import project_root

    log_file = os.path.join(project_root(), "dnd_logger.log")
    handler = RotatingFileHandler(log_file, maxBytes=2 * 1024 * 1024, backupCount=3)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logging.basicConfig(level=logging.DEBUG, handlers=[handler])
    log = logging.getLogger("dndlogger")

    def exception_hook(exc_type, exc_value, exc_tb):
        msg = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        log.critical("Unhandled exception:\n%s", msg)
        print(f"CRASH: {msg}", file=sys.stderr, flush=True)
        sys.__excepthook__(exc_type, exc_value, exc_tb)

    sys.excepthook = exception_hook

    try:
        from PySide6.QtGui import QIcon
        from PySide6.QtWidgets import QApplication
        from src.app import DndLoggerApp
        from src.utils import resource_path

        app = QApplication(sys.argv)
        app.setApplicationName("DnD Logger")
        app.setOrganizationName("DnDLogger")
        app.setApplicationDisplayName("DnD Logger")

        # Set app-wide icon (taskbar + all windows)
        # Prefer PNG — QIcon handles it more reliably than ICO in frozen builds
        icon_path = resource_path("assets/images/app/icon.png")
        if not os.path.exists(icon_path):
            icon_path = resource_path("assets/images/app/icon.ico")
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))

        log.info("Application starting")
        window = DndLoggerApp()
        window.show()
        log.info("Window shown")

        ret = app.exec()
        log.info("Application exited with code %d", ret)
        sys.exit(ret)
    except Exception:
        log.critical("Fatal error:\n%s", traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
