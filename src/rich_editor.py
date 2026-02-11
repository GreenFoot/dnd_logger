"""RichTextEditorWidget — reusable rich-text editor with toolbar and auto-save."""

import os
import re
import shutil

from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QIcon, QPainter, QPen, QPixmap, QTextCharFormat, QTextCursor
from PyQt6.QtWidgets import (
    QComboBox, QHBoxLayout, QPushButton, QTextEdit, QVBoxLayout,
    QWidget,
)


def _make_format_icon(letter: str, style: str = "", size: int = 20) -> QIcon:
    """Draw a formatting icon (B, I, U) with the appropriate visual style."""
    pix = QPixmap(size, size)
    pix.fill(QColor(0, 0, 0, 0))
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    color = QColor(212, 175, 55)  # Gold
    font = QFont("Garamond", 13)
    font.setBold("bold" in style)
    font.setItalic("italic" in style)
    p.setFont(font)
    p.setPen(QPen(color))
    p.drawText(pix.rect(), 0x0084, letter)  # AlignCenter

    if "underline" in style:
        p.setPen(QPen(color, 1.5))
        p.drawLine(3, size - 3, size - 3, size - 3)

    p.end()
    return QIcon(pix)


def _make_save_icon(size: int = 18) -> QIcon:
    """Draw a small floppy/save icon."""
    pix = QPixmap(size, size)
    pix.fill(QColor(0, 0, 0, 0))
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    color = QColor(126, 200, 227)
    p.setPen(QPen(color, 1.5))
    m = 3
    # Floppy body
    p.drawRect(m, m, size - 2 * m, size - 2 * m)
    # Tab at top
    p.drawRect(m + 3, m, size - 2 * m - 6, 4)
    # Label at bottom
    p.drawRect(m + 2, size // 2 + 1, size - 2 * m - 4, size - 2 * m - size // 2)
    p.end()
    return QIcon(pix)


class RichTextEditorWidget(QWidget):
    """Rich-text editor with formatting toolbar and auto-save.

    Subclasses provide ``file_path``, ``default_html``, and
    ``editor_object_name`` via constructor parameters.
    """

    def __init__(self, file_path: str, default_html: str,
                 editor_object_name: str = "rich_editor", parent=None):
        super().__init__(parent)
        self._path = file_path
        self._default_html = default_html
        self._editor_object_name = editor_object_name
        self._save_timer = None
        self._tts_engine = None
        self._build_ui()
        self._load()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Formatting toolbar
        tb_layout = QHBoxLayout()
        tb_layout.setContentsMargins(4, 2, 4, 2)
        tb_layout.setSpacing(4)

        self.btn_bold = QPushButton()
        self.btn_bold.setIcon(_make_format_icon("B", "bold"))
        self.btn_bold.setIconSize(QSize(18, 18))
        self.btn_bold.setToolTip("Gras (Ctrl+B)")
        self.btn_bold.setFixedSize(32, 28)
        self.btn_bold.setCheckable(True)

        self.btn_italic = QPushButton()
        self.btn_italic.setIcon(_make_format_icon("I", "italic"))
        self.btn_italic.setIconSize(QSize(18, 18))
        self.btn_italic.setToolTip("Italique (Ctrl+I)")
        self.btn_italic.setFixedSize(32, 28)
        self.btn_italic.setCheckable(True)

        self.btn_underline = QPushButton()
        self.btn_underline.setIcon(_make_format_icon("U", "underline"))
        self.btn_underline.setIconSize(QSize(18, 18))
        self.btn_underline.setToolTip("Souligner (Ctrl+U)")
        self.btn_underline.setFixedSize(32, 28)
        self.btn_underline.setCheckable(True)

        self.heading_combo = QComboBox()
        self.heading_combo.addItems(["Normal", "Titre 1", "Titre 2", "Titre 3"])
        self.heading_combo.setFixedWidth(110)

        self.btn_save = QPushButton(" Sauvegarder")
        self.btn_save.setIcon(_make_save_icon())
        self.btn_save.setIconSize(QSize(16, 16))
        self.btn_save.setObjectName("btn_primary")

        for w in (self.btn_bold, self.btn_italic, self.btn_underline,
                  self.heading_combo, self.btn_save):
            tb_layout.addWidget(w)
        tb_layout.addStretch()

        layout.addLayout(tb_layout)

        # Editor
        self.editor = QTextEdit()
        self.editor.setObjectName(self._editor_object_name)
        self.editor.setAcceptRichText(True)
        self.editor.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.editor.customContextMenuRequested.connect(self._on_editor_context_menu)
        doc_font = QFont("Cinzel", 12)
        doc_font.setStyleHint(QFont.StyleHint.Serif)
        self.editor.document().setDefaultFont(doc_font)
        layout.addWidget(self.editor)

        # Signals
        self.btn_bold.clicked.connect(self._toggle_bold)
        self.btn_italic.clicked.connect(self._toggle_italic)
        self.btn_underline.clicked.connect(self._toggle_underline)
        self.heading_combo.currentIndexChanged.connect(self._set_heading)
        self.btn_save.clicked.connect(self.save)
        self.editor.textChanged.connect(self._schedule_autosave)

    def _toggle_bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Weight.Bold if self.btn_bold.isChecked() else QFont.Weight.Normal)
        self.editor.mergeCurrentCharFormat(fmt)

    def _toggle_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.btn_italic.isChecked())
        self.editor.mergeCurrentCharFormat(fmt)

    def _toggle_underline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.btn_underline.isChecked())
        self.editor.mergeCurrentCharFormat(fmt)

    def _set_heading(self, index: int):
        cursor = self.editor.textCursor()
        cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
        fmt = QTextCharFormat()
        if index == 0:  # Normal
            fmt.setFontPointSize(13)
            fmt.setFontWeight(QFont.Weight.Normal)
        elif index == 1:  # H1
            fmt.setFontPointSize(22)
            fmt.setFontWeight(QFont.Weight.Bold)
        elif index == 2:  # H2
            fmt.setFontPointSize(18)
            fmt.setFontWeight(QFont.Weight.Bold)
        elif index == 3:  # H3
            fmt.setFontPointSize(15)
            fmt.setFontWeight(QFont.Weight.Bold)
        cursor.mergeCharFormat(fmt)

    def _schedule_autosave(self):
        if self._save_timer is not None:
            return  # Already scheduled
        self._save_timer = QTimer.singleShot(2000, self._autosave)

    def _autosave(self):
        self._save_timer = None
        self.save()

    @staticmethod
    def _strip_inline_fonts(html: str) -> str:
        """Remove inline font-family declarations so the document default applies."""
        return re.sub(r"\s*font-family:[^;\"']*;?", "", html)

    def _load(self):
        if os.path.exists(self._path):
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    html = self._strip_inline_fonts(f.read())
                self.editor.setHtml(html)
            except OSError:
                self.editor.setHtml(self._default_html)
        else:
            self.editor.setHtml(self._default_html)

    def save(self):
        """Save content to disk with .bak backup."""
        html = self.editor.toHtml()
        if os.path.exists(self._path):
            try:
                shutil.copy2(self._path, self._path + ".bak")
            except OSError:
                pass
        try:
            with open(self._path, "w", encoding="utf-8") as f:
                f.write(html)
        except OSError:
            pass

    def set_tts_engine(self, tts_engine):
        """Set a shared TTS engine for read-aloud context menu."""
        self._tts_engine = tts_engine

    def _on_editor_context_menu(self, pos):
        """Custom context menu with TTS option for selected text."""
        menu = self.editor.createStandardContextMenu()
        selection = self.editor.textCursor().selectedText()
        if selection and self._tts_engine and self._tts_engine.is_available:
            from PyQt6.QtGui import QAction
            menu.addSeparator()
            tts_action = QAction("Lire la selection", menu)
            tts_action.triggered.connect(lambda: self._speak_selection())
            menu.addAction(tts_action)
        menu.exec(self.editor.mapToGlobal(pos))

    def _speak_selection(self):
        """Speak the currently selected text via TTS."""
        cursor = self.editor.textCursor()
        text = cursor.selectedText()
        if text and self._tts_engine and self._tts_engine.is_available:
            self._tts_engine.speak_requested.emit(text)

    def get_compact_context(self) -> str:
        """Return last ~4000 chars of plain text for context chaining."""
        text = self.editor.toPlainText()
        if len(text) > 4000:
            text = text[-4000:]
        return text
