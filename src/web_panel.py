"""D&D Beyond embedded browser panel."""

import glob
import logging
import os

from PySide6.QtCore import QSize, QUrl
from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap
from PySide6.QtWebEngineCore import (
    QWebEnginePage,
    QWebEngineProfile,
    QWebEngineSettings,
    QWebEngineUrlRequestInterceptor,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QStyle,
    QVBoxLayout,
    QWidget,
)

from .utils import browser_data_dir, load_config, save_config

log = logging.getLogger("dndlogger.web")

_CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def _make_icon(draw_func, size=20, color=QColor(126, 200, 227)):
    """Create an icon by drawing on a QPixmap."""
    pix = QPixmap(size, size)
    pix.fill(QColor(0, 0, 0, 0))
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(QPen(color, 1.8))
    draw_func(p, size)
    p.end()
    return QIcon(pix)


def _icon_back(p, s):
    m = s * 0.25
    cx, cy = s / 2, s / 2
    p.drawLine(int(cx + m * 0.3), int(m), int(m), int(cy))
    p.drawLine(int(m), int(cy), int(cx + m * 0.3), int(s - m))
    p.drawLine(int(m), int(cy), int(s - m), int(cy))


def _icon_forward(p, s):
    m = s * 0.25
    cx, cy = s / 2, s / 2
    p.drawLine(int(cx - m * 0.3), int(m), int(s - m), int(cy))
    p.drawLine(int(s - m), int(cy), int(cx - m * 0.3), int(s - m))
    p.drawLine(int(s - m), int(cy), int(m), int(cy))


def _icon_refresh(p, s):
    from PySide6.QtCore import QRectF

    m = s * 0.25
    rect = QRectF(m, m, s - 2 * m, s - 2 * m)
    p.drawArc(rect, 30 * 16, 300 * 16)
    # Arrow head at top-right of arc
    ax, ay = int(s * 0.65), int(m)
    p.drawLine(ax, ay, ax + 4, ay + 4)
    p.drawLine(ax, ay, ax - 3, ay + 4)


def _icon_home(p, s):
    m = s * 0.22
    cx = s / 2
    # Roof
    p.drawLine(int(m), int(s * 0.48), int(cx), int(m))
    p.drawLine(int(cx), int(m), int(s - m), int(s * 0.48))
    # Walls
    p.drawLine(int(m + 2), int(s * 0.48), int(m + 2), int(s - m))
    p.drawLine(int(s - m - 2), int(s * 0.48), int(s - m - 2), int(s - m))
    # Floor
    p.drawLine(int(m + 2), int(s - m), int(s - m - 2), int(s - m))
    # Door
    dw = s * 0.18
    p.drawRect(int(cx - dw / 2), int(s * 0.58), int(dw), int(s - m - s * 0.58))


class _NoBrotliInterceptor(QWebEngineUrlRequestInterceptor):
    """Strip Brotli from Accept-Encoding to work around PyInstaller decompression bug."""

    def interceptRequest(self, info):
        info.setHttpHeader(b"Accept-Encoding", b"gzip, deflate")
        log.debug("Intercepted request: %s", info.requestUrl().toString()[:120])


class _BrowserPage(QWebEnginePage):
    """Main page that redirects popups (OAuth) into the same view."""

    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)

    def createWindow(self, window_type):
        return self

    def javaScriptConsoleMessage(self, level, message, line, source):
        """Capture JS console messages to the app log."""
        level_map = {0: "JS_INFO", 1: "JS_WARN", 2: "JS_ERROR"}
        log.warning("[%s] %s (line %d, %s)", level_map.get(level, "JS"), message, line, source)


class DndBeyondBrowser(QWidget):
    """Embedded browser for D&D Beyond with persistent session."""

    HOME_URL = "https://www.dndbeyond.com"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_profile()
        self._build_ui()

    def _startup_url(self):
        """Return the last visited URL if saved, otherwise the home URL."""
        cfg = load_config()
        last = cfg.get("last_browser_url", "")
        if last and last != "about:blank":
            return last
        return self.HOME_URL

    def _setup_profile(self):
        """Create a named persistent profile for cookies/storage."""
        import sys

        # Migrate old "icewind_dale" profile data to "dnd_logger"
        self._migrate_old_profile()

        self._profile = QWebEngineProfile("dnd_logger", self)

        # In frozen builds, Qt's default storage path is unreliable —
        # point explicitly to %APPDATA% for stable persistence.
        if hasattr(sys, "_MEIPASS"):
            self._profile.setPersistentStoragePath(browser_data_dir())
            self._profile.setCachePath(browser_data_dir() + "/cache")

        self._profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        self._profile.setHttpUserAgent(_CHROME_UA)
        log.info("Profile storage: %s", self._profile.persistentStoragePath())

        # Clean stale locks left by force-killed instances
        self._clean_stale_locks(self._profile.persistentStoragePath())

        # Work around Brotli decompression failure in PyInstaller frozen builds
        if hasattr(sys, "_MEIPASS"):
            self._interceptor = _NoBrotliInterceptor(self)
            self._profile.setUrlRequestInterceptor(self._interceptor)
            log.info("Brotli interceptor installed")

    @staticmethod
    def _migrate_old_profile():
        """Migrate old 'Icewind Dale' app data and profile dirs to current names."""
        import shutil

        local = os.environ.get("LOCALAPPDATA", "")

        # Phase 1: Migrate old "Icewind Dale" app-level data dir into "DnD Logger"
        if local:
            old_app = os.path.join(local, "Icewind Dale")
            new_app = os.path.join(local, "DnD Logger")
            if os.path.isdir(old_app) and not os.path.isdir(new_app):
                try:
                    shutil.move(old_app, new_app)
                    log.info("Migrated app dir %s -> %s", old_app, new_app)
                except OSError as e:
                    log.warning("Failed to migrate app dir: %s", e)

        # Phase 2: Rename old "icewind_dale" profile subdirs to "dnd_logger"
        search_dirs = [browser_data_dir()]
        if local:
            for app_dir in ("DnDLogger", "DnD Logger"):
                search_dirs.append(os.path.join(local, app_dir))

        for base in search_dirs:
            for sub in ("", "QtWebEngine"):
                parent = os.path.join(base, sub) if sub else base
                old = os.path.join(parent, "icewind_dale")
                new = os.path.join(parent, "dnd_logger")
                if os.path.isdir(old) and not os.path.isdir(new):
                    try:
                        shutil.move(old, new)
                        log.info("Migrated profile dir %s -> %s", old, new)
                    except OSError as e:
                        log.warning("Failed to migrate profile dir: %s", e)

    @staticmethod
    def _clean_stale_locks(data_dir):
        """Remove stale Chromium lock files left by force-killed instances."""
        for pattern in ("**/LOCK", "**/lockfile", "**/*.lock"):
            for lock_file in glob.glob(os.path.join(data_dir, pattern), recursive=True):
                try:
                    os.remove(lock_file)
                    log.info("Removed stale lock: %s", lock_file)
                except OSError:
                    pass

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Compact navigation toolbar with drawn icons
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(2, 2, 2, 2)
        nav_layout.setSpacing(2)

        icon_color = QColor(126, 200, 227)

        self.btn_back = QPushButton()
        self.btn_back.setIcon(_make_icon(_icon_back, color=icon_color))
        self.btn_back.setIconSize(QSize(18, 18))
        self.btn_back.setToolTip("Retour")
        self.btn_back.setFixedSize(30, 26)

        self.btn_forward = QPushButton()
        self.btn_forward.setIcon(_make_icon(_icon_forward, color=icon_color))
        self.btn_forward.setIconSize(QSize(18, 18))
        self.btn_forward.setToolTip("Suivant")
        self.btn_forward.setFixedSize(30, 26)

        self.btn_refresh = QPushButton()
        self.btn_refresh.setIcon(_make_icon(_icon_refresh, color=icon_color))
        self.btn_refresh.setIconSize(QSize(18, 18))
        self.btn_refresh.setToolTip("Rafraichir")
        self.btn_refresh.setFixedSize(30, 26)

        self.btn_home = QPushButton()
        self.btn_home.setIcon(_make_icon(_icon_home, color=icon_color))
        self.btn_home.setIconSize(QSize(18, 18))
        self.btn_home.setToolTip("Accueil D&D Beyond")
        self.btn_home.setFixedSize(30, 26)

        for btn in (self.btn_back, self.btn_forward, self.btn_refresh, self.btn_home):
            btn.setObjectName("btn_toolbar")
            nav_layout.addWidget(btn)
        nav_layout.addStretch()

        nav_widget = QWidget()
        nav_widget.setLayout(nav_layout)
        nav_widget.setMaximumHeight(32)
        layout.addWidget(nav_widget)

        # Web view
        self.web_view = QWebEngineView()
        self._page = _BrowserPage(self._profile, self.web_view)
        self.web_view.setPage(self._page)

        settings = self._page.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FocusOnNavigationEnabled, True)

        layout.addWidget(self.web_view)

        # Signals
        self.btn_back.clicked.connect(self.web_view.back)
        self.btn_forward.clicked.connect(self.web_view.forward)
        self.btn_refresh.clicked.connect(self.web_view.reload)
        self.btn_home.clicked.connect(self._go_home)

        self.web_view.setUrl(QUrl(self._startup_url()))

    def _go_home(self):
        self.web_view.setUrl(QUrl(self.HOME_URL))

    def cleanup(self):
        """Save last URL and clean up page before exit."""
        try:
            # Persist the current URL for next launch
            if self._page:
                url = self._page.url().toString()
                if url and url != "about:blank":
                    cfg = load_config()
                    cfg["last_browser_url"] = url
                    save_config(cfg)

            if self._page:
                self._page.setUrl(QUrl("about:blank"))

            # Process pending events so cookie writes complete
            app = QApplication.instance()
            if app:
                app.processEvents()

            if self._page:
                self._page.deleteLater()
                self._page = None

            log.info("Browser cleanup completed")
        except Exception as e:
            log.warning("Browser cleanup error: %s", e)
