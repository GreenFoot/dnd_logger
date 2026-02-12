"""RichTextEditorWidget — reusable rich-text editor with toolbar and auto-save."""

import os
import re
import shutil

from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtGui import (
    QBrush, QColor, QFont, QIcon, QKeySequence, QPainter, QPen, QPixmap,
    QPolygon, QShortcut, QTextCharFormat, QTextCursor, QTextBlock,
)
from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit,
    QVBoxLayout, QWidget,
)

from .fold_manager import FoldManager
from .fold_gutter import FoldGutterWidget, GUTTER_WIDTH


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


def _make_fold_icon(size: int = 18) -> QIcon:
    """Draw a fold-all icon: right-pointing triangle with horizontal lines."""
    pix = QPixmap(size, size)
    pix.fill(QColor(0, 0, 0, 0))
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    gold = QColor("#c9a832")
    p.setPen(QPen(gold))
    p.setBrush(QBrush(gold))
    # Right-pointing triangle (folded)
    cx, cy = 7, size // 2
    p.drawPolygon(QPolygon([
        QPoint(cx - 3, cy - 4),
        QPoint(cx - 3, cy + 4),
        QPoint(cx + 4, cy),
    ]))
    # Two short lines to the right (collapsed content)
    p.setPen(QPen(gold, 1.2))
    p.drawLine(cx + 6, cy - 2, size - 2, cy - 2)
    p.drawLine(cx + 6, cy + 2, size - 2, cy + 2)
    p.end()
    return QIcon(pix)


def _make_unfold_icon(size: int = 18) -> QIcon:
    """Draw an unfold-all icon: down-pointing triangle with horizontal lines."""
    pix = QPixmap(size, size)
    pix.fill(QColor(0, 0, 0, 0))
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    gold = QColor("#c9a832")
    p.setPen(QPen(gold))
    p.setBrush(QBrush(gold))
    # Down-pointing triangle (expanded)
    cx, cy = 7, size // 2
    p.drawPolygon(QPolygon([
        QPoint(cx - 4, cy - 3),
        QPoint(cx + 4, cy - 3),
        QPoint(cx, cy + 4),
    ]))
    # Three short lines to the right (expanded content)
    p.setPen(QPen(gold, 1.2))
    p.drawLine(cx + 6, cy - 4, size - 2, cy - 4)
    p.drawLine(cx + 6, cy, size - 2, cy)
    p.drawLine(cx + 6, cy + 4, size - 2, cy + 4)
    p.end()
    return QIcon(pix)


class _SearchLineEdit(QLineEdit):
    """QLineEdit that forwards Escape and Shift+Enter to the owner editor."""

    def set_editor_widget(self, editor_widget):
        self._editor_widget = editor_widget

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self._editor_widget._close_search()
            return
        if event.key() == Qt.Key.Key_Return and event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self._editor_widget._search_find_prev()
            return
        super().keyPressEvent(event)


class RichTextEditorWidget(QWidget):
    """Rich-text editor with formatting toolbar and auto-save.

    Subclasses provide ``file_path``, ``default_html``, and
    ``editor_object_name`` via constructor parameters.
    """

    def __init__(self, file_path: str, default_html: str,
                 editor_object_name: str = "rich_editor",
                 foldable_heading_levels: set[int] | None = None,
                 fold_by_default: bool = False, parent=None):
        super().__init__(parent)
        self._path = file_path
        self._default_html = default_html
        self._editor_object_name = editor_object_name
        self._foldable_heading_levels = foldable_heading_levels
        self._fold_by_default = fold_by_default
        self._save_timer = None
        self._tts_engine = None
        self._build_ui()
        self._load()

    @staticmethod
    def _detect_heading_level(block: QTextBlock) -> int:
        """Return heading level (1-3) for a block, or 0 for non-headings.

        Detection uses headingLevel() on the block format first (fast path),
        then falls back to char format heuristics (font size + bold).
        """
        # Fast path: explicit heading level on block format
        bf = block.blockFormat()
        hl = bf.headingLevel()
        if hl in (1, 2, 3):
            return hl

        # Fallback: check char format of the first fragment
        it = block.begin()
        if it.atEnd():
            return 0
        fmt = it.fragment().charFormat()
        if fmt.fontWeight() < QFont.Weight.Bold.value:
            return 0
        size = fmt.fontPointSize()
        if size >= 21:
            return 1
        if size >= 17:
            return 2
        if size >= 14.5:
            return 3
        return 0

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

        self.btn_fold_all = QPushButton()
        self.btn_fold_all.setIcon(_make_fold_icon())
        self.btn_fold_all.setIconSize(QSize(18, 18))
        self.btn_fold_all.setToolTip("Replier tout (Ctrl+Shift+-)")
        self.btn_fold_all.setFixedSize(32, 28)

        self.btn_unfold_all = QPushButton()
        self.btn_unfold_all.setIcon(_make_unfold_icon())
        self.btn_unfold_all.setIconSize(QSize(18, 18))
        self.btn_unfold_all.setToolTip("Déplier tout (Ctrl+Shift+=)")
        self.btn_unfold_all.setFixedSize(32, 28)

        self.btn_save = QPushButton(" Sauvegarder")
        self.btn_save.setIcon(_make_save_icon())
        self.btn_save.setIconSize(QSize(16, 16))
        self.btn_save.setObjectName("btn_primary")

        for w in (self.btn_bold, self.btn_italic, self.btn_underline,
                  self.heading_combo, self.btn_fold_all, self.btn_unfold_all,
                  self.btn_save):
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
        self.editor.setViewportMargins(GUTTER_WIDTH, 0, 0, 0)
        layout.addWidget(self.editor)

        # Fold manager + gutter
        self._fold_mgr = FoldManager(
            self.editor.document(), self._detect_heading_level,
            foldable_heading_levels=self._foldable_heading_levels,
            fold_by_default=self._fold_by_default, parent=self,
        )
        self._fold_gutter = FoldGutterWidget(self.editor, self._fold_mgr)

        # Search bar (hidden by default)
        self._search_bar = QWidget()
        self._search_bar.setObjectName("search_bar")
        self._search_bar.setVisible(False)
        sb_layout = QHBoxLayout(self._search_bar)
        sb_layout.setContentsMargins(6, 4, 6, 4)
        sb_layout.setSpacing(4)

        self._search_input = _SearchLineEdit()
        self._search_input.set_editor_widget(self)
        self._search_input.setPlaceholderText("Rechercher…")
        self._search_input.setClearButtonEnabled(True)

        self._search_prev = QPushButton("▲")
        self._search_prev.setFixedSize(28, 28)
        self._search_prev.setToolTip("Précédent (Shift+Enter)")

        self._search_next = QPushButton("▼")
        self._search_next.setFixedSize(28, 28)
        self._search_next.setToolTip("Suivant (Enter)")

        self._search_count = QLabel()
        self._search_count.setObjectName("status_label")
        self._search_count.setMinimumWidth(70)

        self._search_close = QPushButton("✕")
        self._search_close.setFixedSize(28, 28)
        self._search_close.setToolTip("Fermer (Échap)")

        for w in (self._search_input, self._search_prev, self._search_next,
                  self._search_count, self._search_close):
            sb_layout.addWidget(w)

        layout.addWidget(self._search_bar)

        self._search_matches: list[QTextCursor] = []
        self._search_index = -1

        # Signals
        self.btn_bold.clicked.connect(self._toggle_bold)
        self.btn_italic.clicked.connect(self._toggle_italic)
        self.btn_underline.clicked.connect(self._toggle_underline)
        self.heading_combo.currentIndexChanged.connect(self._set_heading)
        self.btn_save.clicked.connect(self.save)
        self.editor.textChanged.connect(self._schedule_autosave)

        # Search signals
        self._search_input.textChanged.connect(self._on_search_changed)
        self._search_input.returnPressed.connect(self._search_find_next)
        self._search_next.clicked.connect(self._search_find_next)
        self._search_prev.clicked.connect(self._search_find_prev)
        self._search_close.clicked.connect(self._close_search)

        # Fold signals
        self.btn_fold_all.clicked.connect(self._fold_all)
        self.btn_unfold_all.clicked.connect(self._unfold_all)

        # Shortcuts
        QShortcut(QKeySequence("Ctrl+F"), self, activated=self._open_search)
        QShortcut(QKeySequence("Ctrl+Shift+["), self, activated=self._fold_current)
        QShortcut(QKeySequence("Ctrl+Shift+]"), self, activated=self._unfold_current)
        QShortcut(QKeySequence("Ctrl+Shift+-"), self, activated=self._fold_all)
        QShortcut(QKeySequence("Ctrl+Shift+="), self, activated=self._unfold_all)

    # ── Search ────────────────────────────────────────────

    def _open_search(self):
        self._search_bar.setVisible(True)
        self._search_input.setFocus()
        self._search_input.selectAll()

    def _close_search(self):
        self._search_bar.setVisible(False)
        self._search_matches.clear()
        self._search_index = -1
        self._search_count.setText("")
        self.editor.setExtraSelections([])
        self.editor.setFocus()

    def _on_search_changed(self, text: str):
        self._search_matches.clear()
        self._search_index = -1
        if not text:
            self._search_count.setText("")
            self.editor.setExtraSelections([])
            return
        doc = self.editor.document()
        cursor = QTextCursor(doc)
        while True:
            cursor = doc.find(text, cursor)
            if cursor.isNull():
                break
            self._search_matches.append(QTextCursor(cursor))
        self._highlight_matches()
        if self._search_matches:
            self._search_index = 0
            self._goto_match()
        else:
            self._search_count.setText("0 résultat")

    def _highlight_matches(self):
        selections = []
        highlight_bg = QColor("#3a3018")
        current_bg = QColor("#6ab4d4")
        for i, cur in enumerate(self._search_matches):
            sel = QTextEdit.ExtraSelection()
            sel.cursor = cur
            if i == self._search_index:
                sel.format.setBackground(current_bg)
                sel.format.setForeground(QColor("#0d0d1e"))
            else:
                sel.format.setBackground(highlight_bg)
            selections.append(sel)
        self.editor.setExtraSelections(selections)

    def _goto_match(self):
        if not self._search_matches:
            return
        self._highlight_matches()
        cur = self._search_matches[self._search_index]
        # Auto-unfold if the match is inside a folded region
        match_block = cur.block().blockNumber()
        self._fold_mgr.ensure_visible(match_block)
        self._fold_gutter.update()
        self.editor.setTextCursor(cur)
        self.editor.ensureCursorVisible()
        total = len(self._search_matches)
        self._search_count.setText(f"{self._search_index + 1}/{total}")

    def _search_find_next(self):
        if not self._search_matches:
            return
        self._search_index = (self._search_index + 1) % len(self._search_matches)
        self._goto_match()

    def _search_find_prev(self):
        if not self._search_matches:
            return
        self._search_index = (self._search_index - 1) % len(self._search_matches)
        self._goto_match()

    # ── Folding ─────────────────────────────────────────────

    def _fold_all(self):
        self._fold_mgr.fold_all()
        self._fold_gutter.update()
        self.editor.viewport().update()

    def _unfold_all(self):
        self._fold_mgr.unfold_all()
        self._fold_gutter.update()
        self.editor.viewport().update()

    def _fold_current(self):
        block_num = self.editor.textCursor().block().blockNumber()
        regions = self._fold_mgr.regions()
        # Fold the region that starts at or contains the cursor
        if block_num in regions:
            self._fold_mgr.fold_at(block_num)
        else:
            for start, r in regions.items():
                if start <= block_num <= r.end:
                    self._fold_mgr.fold_at(start)
                    break
        self._fold_gutter.update()
        self.editor.viewport().update()

    def _unfold_current(self):
        block_num = self.editor.textCursor().block().blockNumber()
        regions = self._fold_mgr.regions()
        if block_num in regions:
            self._fold_mgr.unfold_at(block_num)
        else:
            for start, r in regions.items():
                if start <= block_num <= r.end:
                    self._fold_mgr.unfold_at(start)
                    break
        self._fold_gutter.update()
        self.editor.viewport().update()

    # ── Formatting ────────────────────────────────────────

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
        # Set heading level on block format for fast detection
        from PyQt6.QtGui import QTextBlockFormat
        block_fmt = QTextBlockFormat()
        block_fmt.setHeadingLevel(index)
        cursor.mergeBlockFormat(block_fmt)

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
        """Save content to disk with .bak backup.

        Temporarily unfolds all blocks before toHtml() to ensure no
        content is lost, then restores fold state.
        """
        # Save fold state and unfold everything for a clean export
        fold_state = self._fold_mgr.save_fold_state()
        self._fold_mgr.unfold_all()

        html = self.editor.toHtml()

        # Restore folds
        self._fold_mgr.restore_fold_state(fold_state)
        self._fold_gutter.update()

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
