"""Campaign Assistant — AI-powered Q&A about the campaign using Mistral."""

import re
import time

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
)

from .filigree_overlay import GoldFiligreeOverlay
from .i18n import tr
from .summarizer import _strip_code_fences


def _strip_html(html: str) -> str:
    """Strip HTML tags and collapse whitespace to produce plain text."""
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&mdash;", "—", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&#\d+;", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _get_default_system_prompt() -> str:
    """Return the default campaign assistant system prompt for the current language."""
    return tr("prompt.campaign_assistant")


def get_default_campaign_assistant() -> str:
    """Public accessor for settings UI default prompt."""
    return _get_default_system_prompt()


def _call_with_retry(fn, retries=3, base_delay=15):
    """Call fn() with retry and exponential backoff on 429 rate limit."""
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            if "429" in str(e) and attempt < retries - 1:
                time.sleep(base_delay * (2**attempt))
                continue
            raise


class AssistantWorker(QObject):
    """Runs the AI query in a background thread."""

    answer_ready = Signal(str)
    error = Signal(str)

    def __init__(self, question: str, journal_html: str, quest_log_html: str, config: dict):
        super().__init__()
        self._question = question
        self._journal_html = journal_html
        self._quest_log_html = quest_log_html
        self._config = config

    def run(self):
        """Execute the campaign assistant query."""
        try:
            from mistralai import Mistral

            api_key = self._config.get("api_key", "")
            if not api_key:
                self.error.emit(tr("assistant.error.no_api_key"))
                return

            client = Mistral(api_key=api_key)
            model = self._config.get("summary_model", "mistral-large-latest")

            journal_text = _strip_html(self._journal_html)
            quest_log_text = _strip_html(self._quest_log_html)

            system_template = self._config.get("prompt_campaign_assistant") or _get_default_system_prompt()
            system_prompt = system_template.format(
                language_name=tr("prompt.language_name"),
                quest_log_text=quest_log_text,
                journal_text=journal_text,
            )

            response = _call_with_retry(
                lambda: client.chat.complete(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": self._question},
                    ],
                    temperature=0.2,
                    max_tokens=4000,
                )
            )

            answer = response.choices[0].message.content
            answer = _strip_code_fences(answer)
            self.answer_ready.emit(answer)

        except Exception as e:
            self.error.emit(tr("assistant.error.generic", error=e))


class CampaignAssistantDialog(QDialog):
    """Dialog for asking AI questions about the campaign."""

    def __init__(self, journal_html: str, quest_log_html: str, config: dict, parent=None):
        super().__init__(parent)
        self._journal_html = journal_html
        self._quest_log_html = quest_log_html
        self._config = config
        self._thread = None
        self._worker = None
        self.setWindowTitle(tr("assistant.dialog.title"))
        self.setMinimumSize(600, 400)
        self._build_ui()
        self._filigree = GoldFiligreeOverlay(self)

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Input row
        input_row = QHBoxLayout()
        self._input = QLineEdit()
        self._input.setPlaceholderText(tr("assistant.placeholder"))
        self._input.returnPressed.connect(self._ask)
        input_row.addWidget(self._input, stretch=1)

        self._btn_send = QPushButton(tr("assistant.btn_ask"))
        self._btn_send.setObjectName("btn_primary")
        self._btn_send.clicked.connect(self._ask)
        input_row.addWidget(self._btn_send)
        layout.addLayout(input_row)

        # Status label
        self._status = QLabel("")
        self._status.setStyleSheet("color: #8899aa; font-size: 11px;")
        layout.addWidget(self._status)

        # Answer area
        self._answer = QTextBrowser()
        self._answer.setOpenExternalLinks(False)
        layout.addWidget(self._answer, stretch=1)

    def _ask(self):
        question = self._input.text().strip()
        if not question:
            return

        from .utils import active_campaign_name

        if not active_campaign_name(self._config):
            self._status.setText(tr("assistant.error.no_campaign"))
            self._status.setStyleSheet("color: #ff6b6b; font-size: 11px;")
            return

        self._btn_send.setEnabled(False)
        self._input.setEnabled(False)
        self._status.setText(tr("assistant.thinking"))
        self._status.setStyleSheet("color: #d4af37; font-size: 11px;")
        self._answer.clear()

        self._worker = AssistantWorker(question, self._journal_html, self._quest_log_html, self._config)
        self._thread = QThread()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.answer_ready.connect(self._on_answer)
        self._worker.error.connect(self._on_error)
        self._worker.answer_ready.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.start()

    def _on_answer(self, answer: str):
        self._answer.setHtml(answer)
        self._status.setText("")
        self._btn_send.setEnabled(True)
        self._input.setEnabled(True)
        self._input.setFocus()

    def _on_error(self, error: str):
        self._status.setText(error)
        self._status.setStyleSheet("color: #ff6b6b; font-size: 11px;")
        self._btn_send.setEnabled(True)
        self._input.setEnabled(True)
