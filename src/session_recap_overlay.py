"""SessionRecapOverlay — 'Last time on...' card shown on startup."""

import logging
import os
import re

from PySide6.QtCore import QEvent, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .i18n import tr
from .utils import active_campaign_name, journal_path

log = logging.getLogger(__name__)

# Maximum words shown in the excerpt
_MAX_WORDS = 300

# Auto-dismiss timeout (ms)
_AUTO_DISMISS_MS = 60_000


def _extract_last_session(journal_html: str) -> tuple[str, str] | None:
    """Extract the last <h2> section from journal HTML.

    Returns:
        (heading_text, body_html) or None if no session found.
    """
    # Find all <h2> tags — each marks a session entry
    h2_pattern = re.compile(r"<h2[^>]*>(.*?)</h2>", re.IGNORECASE | re.DOTALL)
    matches = list(h2_pattern.finditer(journal_html))
    if not matches:
        return None

    last_match = matches[-1]
    heading_text = re.sub(r"<[^>]+>", "", last_match.group(1)).strip()

    # Body = everything after the last <h2>...</h2> until end or next <h1>/<h2>
    body_start = last_match.end()
    next_heading = re.search(r"<h[12][^>]*>", journal_html[body_start:], re.IGNORECASE)
    if next_heading:
        body_end = body_start + next_heading.start()
    else:
        body_end = len(journal_html)

    body_html = journal_html[body_start:body_end].strip()
    # Strip trailing <hr> tags
    body_html = re.sub(r"(<hr\s*/?>)+\s*$", "", body_html, flags=re.IGNORECASE).strip()

    if not body_html:
        return None

    # Keep only content after the first <h3> title (the narrative body)
    first_h3_end = re.search(r"</h3>", body_html, re.IGNORECASE)
    if first_h3_end:
        after_h3 = body_html[first_h3_end.end() :]
        next_h3 = re.search(r"<h3[^>]*>", after_h3, re.IGNORECASE)
        if next_h3:
            after_h3 = after_h3[: next_h3.start()]
        body_html = after_h3.strip()

    if not body_html:
        return None

    return heading_text, body_html


def _truncate_words(html: str, max_words: int) -> str:
    """Truncate HTML text to approximately max_words, adding ellipsis."""
    plain = re.sub(r"<[^>]+>", " ", html)
    words = plain.split()
    if len(words) <= max_words:
        return html
    count = 0
    pos = 0
    in_tag = False
    for i, ch in enumerate(html):
        if ch == "<":
            in_tag = True
        elif ch == ">":
            in_tag = False
        elif not in_tag and ch in (" ", "\n", "\t"):
            count += 1
            if count >= max_words:
                pos = i
                break
    else:
        return html

    truncated = html[:pos].rstrip()
    truncated = re.sub(r"<[^>]*$", "", truncated)
    return truncated + "\u2026"


class SessionRecapOverlay(QWidget):
    """Semi-transparent overlay showing the last session recap.

    Uses real QWidgets so the card inherits the app's QSS theme.

    Signals:
        read_aloud_requested: emitted with the summary HTML text.
        dismissed: emitted when the user closes the card.
    """

    read_aloud_requested = Signal(str)
    dismissed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._heading = ""
        self._full_html = ""
        self._campaign = ""

        self._dismiss_timer = QTimer(self)
        self._dismiss_timer.setSingleShot(True)
        self._dismiss_timer.setInterval(_AUTO_DISMISS_MS)
        self._dismiss_timer.timeout.connect(self._on_dismiss)

        self._build_card()

        if parent:
            parent.installEventFilter(self)

        self.hide()

    # ── Card layout (real widgets) ─────────────────────

    def _build_card(self):
        """Build the card UI using themed widgets."""
        # Outer layout centres the card
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addStretch()

        h_center = QHBoxLayout()
        h_center.addStretch()

        # Card frame — picks up QGroupBox-like styling from QSS
        self._card = QFrame(self)
        self._card.setObjectName("recap_card")
        self._card.setFixedWidth(560)
        self._card.setMaximumHeight(480)
        self._card.setStyleSheet(
            "#recap_card {"
            "  background-color: #121a22;"
            "  border: 1px solid #253545;"
            "  border-radius: 8px;"
            "  padding: 0px;"
            "}"
        )

        card_layout = QVBoxLayout(self._card)
        card_layout.setContentsMargins(24, 20, 24, 16)
        card_layout.setSpacing(8)

        # Title label — uses heading object name for QSS
        self._title_label = QLabel()
        self._title_label.setObjectName("subheading")
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._title_label.setWordWrap(True)
        card_layout.addWidget(self._title_label)

        # Gold divider
        div1 = QFrame()
        div1.setFrameShape(QFrame.Shape.HLine)
        div1.setStyleSheet("color: #253545;")
        card_layout.addWidget(div1)

        # Summary text — read-only QTextEdit to match journal/summary styling
        self._summary_display = QTextEdit()
        self._summary_display.setObjectName("summary_display")
        self._summary_display.setReadOnly(True)
        self._summary_display.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._summary_display.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._summary_display.setMinimumHeight(180)
        card_layout.addWidget(self._summary_display, 1)

        # Lower divider
        div2 = QFrame()
        div2.setFrameShape(QFrame.Shape.HLine)
        div2.setStyleSheet("color: #253545;")
        card_layout.addWidget(div2)

        # Session date info
        self._info_label = QLabel()
        self._info_label.setObjectName("status_label")
        self._info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self._info_label)

        # Buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self._read_btn = QPushButton(tr("recap.btn.read_aloud"))
        self._read_btn.setObjectName("btn_gold")
        self._read_btn.clicked.connect(self._on_read_aloud)
        btn_row.addWidget(self._read_btn)

        self._dismiss_btn = QPushButton(tr("recap.btn.dismiss"))
        self._dismiss_btn.clicked.connect(self._on_dismiss)
        btn_row.addWidget(self._dismiss_btn)

        card_layout.addLayout(btn_row)

        # Keyboard hints
        self._hints_label = QLabel(f"{tr('recap.hint.read')}  \u2502  {tr('recap.hint.dismiss')}")
        self._hints_label.setObjectName("status_label")
        self._hints_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self._hints_label)

        h_center.addWidget(self._card)
        h_center.addStretch()
        outer.addLayout(h_center)
        outer.addStretch()

    # ── Public API ─────────────────────────────────────

    def show_recap(self, config: dict):
        """Parse journal and show recap if a session exists.

        Args:
            config: Application config dict (used for paths and campaign name).
        """
        if not config.get("show_session_recap", True):
            return

        jp = journal_path(config)
        if not os.path.isfile(jp):
            return

        try:
            with open(jp, "r", encoding="utf-8") as f:
                html = f.read()
        except OSError:
            return

        result = _extract_last_session(html)
        if result is None:
            return

        heading, body = result

        # Check if we already showed this session
        last_shown = config.get("last_recap_heading", "")
        if last_shown == heading:
            return

        campaign = active_campaign_name(config)
        self._heading = heading
        self._full_html = body
        self._campaign = campaign

        # Populate widgets
        self._title_label.setText(tr("recap.title", campaign=campaign))
        self._summary_display.setHtml(_truncate_words(body, _MAX_WORDS))
        self._info_label.setText(heading)

        self._sync_geometry()
        self.raise_()
        self.show()
        self.setFocus()
        self._dismiss_timer.start()

    def hide_recap(self):
        """Hide the overlay."""
        self._dismiss_timer.stop()
        self.hide()
        self.dismissed.emit()

    # ── Event handling ─────────────────────────────────

    def keyPressEvent(self, event):
        """Escape to dismiss, Space to read aloud."""
        if event.key() == Qt.Key.Key_Escape:
            self._on_dismiss()
        elif event.key() == Qt.Key.Key_Space:
            self._on_read_aloud()
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        """Click outside card to dismiss."""
        card_geo = self._card.geometry()
        if not card_geo.contains(event.position().toPoint()):
            self._on_dismiss()

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

    def _on_dismiss(self):
        """Dismiss the card and mark as shown."""
        self.hide_recap()

    def _on_read_aloud(self):
        """Emit read-aloud signal and dismiss."""
        if self._full_html:
            self.read_aloud_requested.emit(self._full_html)
        self.hide_recap()
