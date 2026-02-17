"""AI quest extraction from session summaries via Mistral API."""

import re

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QTextEdit,
    QVBoxLayout,
)

from .diff_utils import apply_inline_diff, extract_html_without_deleted
from .i18n import tr
from .summarizer import _resolve_prompt


def _get_extraction_prompt() -> str:
    """Return the resolved quest extraction prompt for the current language."""
    return _resolve_prompt(tr("prompt.quest_extraction"))


# Module-level alias used by settings.py for prompt defaults
def get_default_quest_extraction() -> str:
    return _get_extraction_prompt()


def _strip_model_artifacts(text: str) -> str:
    """Remove code fences and markdown formatting the model sometimes adds."""
    text = text.strip()
    text = re.sub(r"^```html\s*\n?", "", text)
    text = re.sub(r"\n?```\s*$", "", text)
    text = re.sub(r"\n---\n", "\n", text)
    text = re.sub(r"\n---$", "", text)
    text = re.sub(r"^---\n", "", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    return text.strip()


class QuestExtractorWorker(QObject):
    """Extracts quest updates from a session summary via Mistral API."""

    completed = Signal(str)  # quest update HTML
    error = Signal(str)

    def __init__(self, summary_html: str, current_quests: str, config: dict,
                 campaign_name: str = ""):
        super().__init__()
        self._summary = summary_html
        self._current_quests = current_quests
        self._config = config
        self._campaign_name = campaign_name

    def run(self):
        try:
            from mistralai import Mistral

            api_key = self._config.get("api_key", "")
            if not api_key:
                self.error.emit(tr("quest_extractor.error.no_api_key"))
                return

            client = Mistral(api_key=api_key)
            model = self._config.get("summary_model", "mistral-large-latest")

            extraction_template = self._config.get("prompt_quest_extraction") or _get_extraction_prompt()
            prompt = extraction_template.format(
                campaign_name=self._campaign_name or "D&D",
                current_quests=self._current_quests or tr("quest_extractor.no_quests"),
                summary=self._summary,
            )

            response = client.chat.complete(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=16000,
            )

            result = _strip_model_artifacts(response.choices[0].message.content)
            self.completed.emit(result)

        except Exception as e:
            self.error.emit(tr("quest_extractor.error.generic", error=e))


class QuestProposalDialog(QDialog):
    """Editable unified-diff preview of AI-proposed quest updates.

    Shows a single view with deleted lines inline (red + strikethrough) and
    added/changed lines highlighted green.  The user can edit freely; on
    accept the deleted-marked lines are stripped and the remaining rich-text
    HTML is returned.
    """

    def __init__(self, proposed_html: str, current_html: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("quest_extractor.dialog_title"))
        self.setMinimumSize(700, 500)

        # Render current HTML through the same Qt pipeline used for proposed,
        # so line splitting is consistent for diffing.
        self._current_lines: list[str] = []
        if current_html:
            tmp = QTextEdit()
            tmp.setHtml(current_html)
            self._current_lines = tmp.toPlainText().split("\n")

        layout = QVBoxLayout(self)

        label = QLabel(tr("quest_extractor.dialog_label"))
        label.setObjectName("subheading")
        layout.addWidget(label)

        self.editor = QTextEdit()
        self.editor.setHtml(proposed_html)
        self.editor.setAcceptRichText(True)
        layout.addWidget(self.editor, stretch=1)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        apply_inline_diff(self.editor, self._current_lines)

    def get_html(self) -> str:
        """Return quest HTML with deleted-marked lines stripped and highlights cleared."""
        return extract_html_without_deleted(self.editor)


def start_quest_extraction(
    summary_html: str, current_quests: str, config: dict,
    campaign_name: str = "",
) -> tuple[QThread, QuestExtractorWorker]:
    """Create a quest extraction worker in a new thread."""
    thread = QThread()
    worker = QuestExtractorWorker(summary_html, current_quests, config,
                                  campaign_name=campaign_name)
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.completed.connect(thread.quit)
    worker.error.connect(thread.quit)
    return thread, worker
