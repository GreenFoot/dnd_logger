"""ShortcutsOverlay — themed keyboard shortcuts cheat-sheet."""

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .i18n import tr

_SHORTCUTS = [
    (
        "shortcuts.group.general",
        [
            ("Ctrl+,", "shortcuts.settings"),
            ("Ctrl+S", "shortcuts.save"),
            ("Ctrl+Q", "shortcuts.quit"),
            ("F1", "shortcuts.help"),
        ],
    ),
    (
        "shortcuts.group.recording",
        [
            ("Ctrl+R", "shortcuts.record"),
            ("F2", "shortcuts.bookmark"),
            ("Ctrl+Shift+F", "shortcuts.ask_campaign"),
        ],
    ),
    (
        "shortcuts.group.editor",
        [
            ("Ctrl+F", "shortcuts.find"),
            ("Ctrl+B", "shortcuts.bold"),
            ("Ctrl+I", "shortcuts.italic"),
            ("Ctrl+U", "shortcuts.underline"),
            ("Ctrl+Shift+[", "shortcuts.fold_section"),
            ("Ctrl+Shift+]", "shortcuts.unfold_section"),
            ("Ctrl+Shift+-", "shortcuts.fold_all"),
            ("Ctrl+Shift+=", "shortcuts.unfold_all"),
        ],
    ),
    (
        "shortcuts.group.tts",
        [
            ("Space", "shortcuts.tts_pause"),
            ("Escape", "shortcuts.tts_stop"),
        ],
    ),
]


def _split_combo(combo: str) -> list[str]:
    """Split a key combo like 'Ctrl+Shift+,' into individual key labels."""
    parts = combo.split("+")
    result = []
    for part in parts:
        if part:
            result.append(part)
    return result


class ShortcutsOverlay(QWidget):
    """Full-window overlay showing all keyboard shortcuts.

    Uses real QWidgets so the card inherits the app's QSS theme,
    with a QScrollArea for the shortcut list.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._prev_focus = None

        self._build_card()

        if parent:
            parent.installEventFilter(self)

        self.hide()

    # ── Card layout (real widgets) ─────────────────────

    def _build_card(self):
        """Build the card UI using themed widgets."""
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addStretch()

        h_center = QHBoxLayout()
        h_center.addStretch()

        # Card frame
        self._card = QFrame(self)
        self._card.setObjectName("shortcuts_card")
        self._card.setFixedWidth(500)
        self._card.setMaximumHeight(480)
        self._card.setStyleSheet(
            "#shortcuts_card {"
            "  background-color: #121a22;"
            "  border: 1px solid #253545;"
            "  border-radius: 8px;"
            "  padding: 0px;"
            "}"
        )

        card_layout = QVBoxLayout(self._card)
        card_layout.setContentsMargins(24, 20, 24, 16)
        card_layout.setSpacing(8)

        # Title
        self._title_label = QLabel()
        self._title_label.setObjectName("subheading")
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self._title_label)

        # Divider under title
        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet("color: #253545;")
        card_layout.addWidget(div)

        # Scrollable shortcut content
        scroll = QScrollArea()
        scroll.setObjectName("shortcuts_scroll")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet(
            "#shortcuts_scroll { background: transparent; border: none; }"
            "#shortcuts_scroll QScrollBar:vertical {"
            "  background: #0d1117; width: 6px; border-radius: 3px;"
            "}"
            "#shortcuts_scroll QScrollBar::handle:vertical {"
            "  background: #253545; border-radius: 3px; min-height: 20px;"
            "}"
            "#shortcuts_scroll QScrollBar::add-line:vertical,"
            "#shortcuts_scroll QScrollBar::sub-line:vertical { height: 0px; }"
        )

        self._content_widget = QWidget()
        self._content_widget.setStyleSheet("background: transparent;")
        self._content_layout = QVBoxLayout(self._content_widget)
        self._content_layout.setContentsMargins(4, 4, 4, 4)
        self._content_layout.setSpacing(0)
        scroll.setWidget(self._content_widget)

        card_layout.addWidget(scroll, 1)

        # Dismiss hint
        hint = QLabel("Esc / F1")
        hint.setObjectName("status_label")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(hint)

        h_center.addWidget(self._card)
        h_center.addStretch()
        outer.addLayout(h_center)
        outer.addStretch()

    def _populate_shortcuts(self):
        """Populate the shortcut list from the _SHORTCUTS data structure."""
        # Clear previous content
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for gi, (group_key, shortcuts) in enumerate(_SHORTCUTS):
            if gi > 0:
                # Divider between groups
                div = QFrame()
                div.setFrameShape(QFrame.Shape.HLine)
                div.setFixedHeight(1)
                div.setStyleSheet("background-color: rgba(212, 175, 55, 60); border: none; margin: 6px 0px;")
                self._content_layout.addWidget(div)

            # Group header
            header = QLabel(tr(group_key))
            header.setStyleSheet(
                "font-family: Cinzel; font-size: 12px; font-weight: bold;"
                " color: #7ec8e3; padding: 4px 0px 2px 0px; background: transparent;"
            )
            self._content_layout.addWidget(header)

            # Shortcut rows
            for key_combo, desc_key in shortcuts:
                row = QHBoxLayout()
                row.setContentsMargins(0, 1, 0, 1)
                row.setSpacing(0)

                keys_container = QHBoxLayout()
                keys_container.setContentsMargins(0, 0, 12, 0)
                keys_container.setSpacing(3)
                keys_container.addStretch()
                for part in _split_combo(key_combo):
                    kbd = QLabel(part)
                    kbd.setStyleSheet(
                        "font-family: Consolas; font-size: 10px; color: #c8e6f0;"
                        " background-color: #1e2d3d; border: 1px solid #35506a;"
                        " border-radius: 3px; padding: 1px 5px;"
                    )
                    keys_container.addWidget(kbd)

                keys_widget = QWidget()
                keys_widget.setFixedWidth(170)
                keys_widget.setLayout(keys_container)
                keys_widget.setStyleSheet("background: transparent;")

                desc_label = QLabel(tr(desc_key))
                desc_label.setStyleSheet(
                    "font-family: Cinzel; font-size: 11px; color: #e6dcc8;"
                    " padding: 2px 0px; background: transparent;"
                )

                row.addWidget(keys_widget)
                row.addWidget(desc_label, 1)

                row_widget = QWidget()
                row_widget.setLayout(row)
                row_widget.setStyleSheet("background: transparent;")
                self._content_layout.addWidget(row_widget)

        self._content_layout.addStretch()

    # ── Public API ─────────────────────────────────────

    def show_overlay(self):
        """Show the shortcuts overlay."""
        if not self.isVisible():
            from PySide6.QtWidgets import QApplication

            self._prev_focus = QApplication.focusWidget()
        self._title_label.setText(tr("shortcuts.title"))
        self._populate_shortcuts()
        self._sync_geometry()
        self.raise_()
        self.show()
        self.setFocus()

    def hide_overlay(self):
        """Hide the overlay and restore focus."""
        self.hide()
        if self._prev_focus and not self._prev_focus.isHidden():
            self._prev_focus.setFocus()
        self._prev_focus = None

    # ── Event handling ─────────────────────────────────
    # Note: F1 dismiss is handled by the toggle action in app.py,
    # and Escape dismiss is handled by the global Escape shortcut in app.py.

    def mousePressEvent(self, event):
        """Click outside card to dismiss."""
        card_geo = self._card.geometry()
        if not card_geo.contains(event.position().toPoint()):
            self.hide_overlay()

    def eventFilter(self, obj, event):
        """Resize overlay when parent resizes."""
        if obj == self.parentWidget() and event.type() == QEvent.Type.Resize:
            if self.isVisible():
                self._sync_geometry()
        return False

    def paintEvent(self, event):
        """Draw only the semi-transparent dim background."""
        p = QPainter(self)
        p.fillRect(self.rect(), QColor(13, 13, 30, 160))
        p.end()

    # ── Private ────────────────────────────────────────

    def _sync_geometry(self):
        parent = self.parentWidget()
        if parent:
            self.setGeometry(0, 0, parent.width(), parent.height())
