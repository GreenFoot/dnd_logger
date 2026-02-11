"""IcewindDaleApp — main window."""

import os
import shutil

from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import (
    QAction,
    QBrush,
    QFontDatabase,
    QIcon,
    QKeySequence,
    QPalette,
    QPixmap,
    QShortcut,
)
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QSplitter, QTabWidget

from .frost_overlay import GoldFiligreeOverlay
from .journal import JournalWidget
from .quest_log import QuestLogWidget
from .session_tab import SessionTab
from .settings import FirstRunWizard, SettingsDialog
from .tts_engine import create_tts_thread
from .utils import journal_path, load_config, quest_log_path, resource_path, save_config
from .web_panel import DndBeyondBrowser


class IcewindDaleApp(QMainWindow):
    """Main application window with split layout."""

    def __init__(self):
        super().__init__()
        self._config = load_config()
        self._load_icon()
        self._load_fonts()
        self._load_stylesheet()
        self._migrate_journal()
        self._init_tts()
        self._build_ui()
        self._apply_backgrounds()
        self._add_decorative_overlays()
        self._build_menu()
        self._restore_geometry()
        self._check_first_run()

    def _load_icon(self):
        """Set the D20 window/taskbar icon."""
        icon_path = resource_path("assets/images/icon.png")
        if not os.path.exists(icon_path):
            icon_path = resource_path("assets/images/icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _load_fonts(self):
        """Load custom fonts from assets."""
        fonts_dir = resource_path("assets/fonts")
        if os.path.isdir(fonts_dir):
            for fname in os.listdir(fonts_dir):
                if fname.lower().endswith((".ttf", ".otf")):
                    QFontDatabase.addApplicationFont(os.path.join(fonts_dir, fname))

    def _load_stylesheet(self):
        """Load the Icewind Dale QSS theme."""
        qss_path = resource_path("assets/styles/icewind.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def _init_tts(self):
        """Initialize a shared TTS engine for all widgets."""
        self._tts_thread, self._tts_engine = create_tts_thread()
        self._tts_engine.error.connect(self._on_tts_error)
        self._tts_thread.start()
        # Escape key stops TTS playback
        self._tts_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        self._tts_shortcut.activated.connect(self._stop_tts)

    def _stop_tts(self):
        """Stop TTS playback on Escape key."""
        if self._tts_engine:
            self._tts_engine.stop()

    def _on_tts_error(self, msg: str):
        """Show TTS errors in the status bar."""
        self.statusBar().showMessage(msg, 5000)

    def _migrate_journal(self):
        """One-time migration: copy existing quest log content to journal."""
        j_path = journal_path(self._config)
        ql_path = quest_log_path(self._config)

        if os.path.exists(j_path):
            return  # Already migrated

        if not os.path.exists(ql_path):
            return  # Nothing to migrate

        # Check if quest log has session entries (contains "Session du")
        try:
            with open(ql_path, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError:
            return

        if "Session du" in content:
            # Copy quest log content to journal
            try:
                shutil.copy2(ql_path, j_path)
            except OSError:
                return
            # Reset quest log to new default (will happen naturally when
            # QuestLogWidget loads and finds no file after we remove the old one)
            try:
                bak = ql_path + ".pre_migration.bak"
                shutil.copy2(ql_path, bak)
                os.remove(ql_path)
            except OSError:
                pass

    def _apply_backgrounds(self):
        """Apply background textures to widgets."""
        # Main window background: prefer downloaded landscape, fall back to generated
        bg_path = resource_path("assets/images/frost_bg.png")
        if not os.path.exists(bg_path):
            bg_path = resource_path("assets/images/frost_bg_generated.png")
        if os.path.exists(bg_path):
            palette = self.palette()
            bg_pix = QPixmap(bg_path)
            if not bg_pix.isNull():
                palette.setBrush(QPalette.ColorRole.Window, QBrush(bg_pix))
                self.setPalette(palette)
                self.setAutoFillBackground(True)

        # Parchment texture on journal and quest log editors
        parch_path = resource_path("assets/images/parchment_warm.png")
        if not os.path.exists(parch_path):
            parch_path = resource_path("assets/images/parchment_bg.png")
        if os.path.exists(parch_path):
            parch_pix = QPixmap(parch_path)
            if not parch_pix.isNull():
                for editor in (self.journal.editor, self.quest_log.editor):
                    p = editor.palette()
                    p.setBrush(QPalette.ColorRole.Base, QBrush(parch_pix))
                    editor.setPalette(p)
                    editor.setAutoFillBackground(True)

        # Summary texture (prefer processed over generated)
        summary_path = resource_path("assets/images/summary_bg.png")
        if not os.path.exists(summary_path):
            summary_path = resource_path("assets/images/summary_bg_generated.png")
        if os.path.exists(summary_path):
            summary = self.session_tab.summary_display
            p = summary.palette()
            summary_pix = QPixmap(summary_path)
            if not summary_pix.isNull():
                p.setBrush(QPalette.ColorRole.Base, QBrush(summary_pix))
                summary.setPalette(p)
                summary.setAutoFillBackground(True)

    def _add_decorative_overlays(self):
        """Add gold filigree corner decorations to key panels."""
        self._journal_filigree = GoldFiligreeOverlay(self.journal)
        self._quest_filigree = GoldFiligreeOverlay(self.quest_log)
        self._session_filigree = GoldFiligreeOverlay(self.session_tab)

    def _build_ui(self):
        self.setWindowTitle("Icewind Dale — D&D Session Logger")
        self.setMinimumSize(1200, 700)

        # Main splitter: left (browser) | right (tabs)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel: D&D Beyond browser
        self.browser = DndBeyondBrowser()
        self.splitter.addWidget(self.browser)

        # Right panel: tabs
        self.right_tabs = QTabWidget()

        self.journal = JournalWidget(self._config)
        self.journal.set_tts_engine(self._tts_engine)
        self.quest_log = QuestLogWidget(self._config)
        self.quest_log.set_tts_engine(self._tts_engine)

        # Tab icons
        quill_icon_path = resource_path("assets/images/tab_icon_questlog.png")
        crystal_icon_path = resource_path("assets/images/tab_icon_session.png")

        # Journal tab (first)
        if os.path.exists(quill_icon_path):
            self.right_tabs.addTab(self.journal, QIcon(quill_icon_path), "Journal")
        else:
            self.right_tabs.addTab(self.journal, "Journal")

        # Quest Log tab (second)
        if os.path.exists(quill_icon_path):
            self.right_tabs.addTab(self.quest_log, QIcon(quill_icon_path), "Quest Log")
        else:
            self.right_tabs.addTab(self.quest_log, "Quest Log")

        # Session tab (third)
        self.session_tab = SessionTab(
            self._config,
            journal_widget=self.journal,
            quest_log_widget=self.quest_log,
            tts_engine=self._tts_engine,
        )

        if os.path.exists(crystal_icon_path):
            self.right_tabs.addTab(self.session_tab, QIcon(crystal_icon_path), "Session")
        else:
            self.right_tabs.addTab(self.session_tab, "Session")

        self.splitter.addWidget(self.right_tabs)

        # 55/45 split
        self.splitter.setSizes([600, 500])

        self.setCentralWidget(self.splitter)

    def _build_menu(self):
        menu_bar = self.menuBar()

        # Fichier menu
        file_menu = menu_bar.addMenu("Fichier")

        settings_action = QAction("Paramètres...", self)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.triggered.connect(self._open_settings)
        file_menu.addAction(settings_action)

        file_menu.addSeparator()

        save_action = QAction("Sauvegarder", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self._save_active_editor)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        quit_action = QAction("Quitter", self)
        quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Session menu
        session_menu = menu_bar.addMenu("Session")

        record_action = QAction("Enregistrer / Arrêter", self)
        record_action.setShortcut(QKeySequence("Ctrl+R"))
        record_action.triggered.connect(self._toggle_recording)
        session_menu.addAction(record_action)

    def _save_active_editor(self):
        """Save whichever editor tab is currently active."""
        current = self.right_tabs.currentWidget()
        if current is self.journal:
            self.journal.save()
        elif current is self.quest_log:
            self.quest_log.save()

    def _check_first_run(self):
        """Show first-run wizard if API key is empty."""
        if not self._config.get("api_key"):
            wizard = FirstRunWizard(self._config, self)
            if wizard.exec():
                self._config = wizard.get_config()
                self._refresh_config()

    def _open_settings(self):
        dlg = SettingsDialog(self._config, self)
        if dlg.exec():
            self._config = dlg.get_config()
            self._refresh_config()

    def _refresh_config(self):
        """Push updated config to child widgets."""
        self.session_tab.update_config(self._config)

    def _toggle_recording(self):
        """Toggle recording from keyboard shortcut."""
        rec = self.session_tab._recorder
        if rec.is_recording:
            self.session_tab._stop_recording()
        else:
            self.session_tab._start_recording()
        # Switch to Session tab
        self.right_tabs.setCurrentWidget(self.session_tab)

    def _restore_geometry(self):
        """Restore window size/position from QSettings."""
        settings = QSettings("IcewindDale", "DndLogger")
        geo = settings.value("geometry")
        if geo:
            self.restoreGeometry(geo)
        state = settings.value("windowState")
        if state:
            self.restoreState(state)

    def _save_geometry(self):
        """Save window size/position."""
        settings = QSettings("IcewindDale", "DndLogger")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())

    def closeEvent(self, event):
        """Clean up on exit."""
        self._save_geometry()
        self.journal.save()
        self.quest_log.save()
        self.session_tab.cleanup()
        self.browser.cleanup()
        # Shut down shared TTS
        if self._tts_engine:
            self._tts_engine.stop()
        if self._tts_thread and self._tts_thread.isRunning():
            self._tts_thread.quit()
            self._tts_thread.wait(2000)
        # Give QWebEngine a moment to flush cookies/storage to disk
        from PyQt6.QtCore import QElapsedTimer

        timer = QElapsedTimer()
        timer.start()
        app = QApplication.instance()
        while timer.elapsed() < 500:
            if app:
                app.processEvents()
        event.accept()
