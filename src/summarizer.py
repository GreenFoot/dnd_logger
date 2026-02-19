"""Summarization via Mistral chat API with epic fantasy style."""

import re
import time

from PySide6.QtCore import QObject, QThread, Signal

from .i18n import tr


def _strip_code_fences(text: str) -> str:
    """Remove code fences and formatting artifacts that models sometimes add."""
    text = text.strip()
    text = re.sub(r"^```html\s*\n?", "", text)
    text = re.sub(r"\n?```\s*$", "", text)
    # Strip markdown horizontal rules
    text = re.sub(r"\n---\n", "\n", text)
    text = re.sub(r"\n---$", "", text)
    text = re.sub(r"^---\n", "", text)
    # Convert markdown bold **text** to <strong>text</strong>
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Convert markdown italic *text* to <em>text</em> (single asterisks)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    return text.strip()


class _PartialFormatMap(dict):
    """Dict subclass that leaves unknown {keys} untouched during format_map."""

    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def _resolve_prompt(prompt_template: str) -> str:
    """Resolve a prompt template by filling in section headers and language.

    Runtime placeholders like {text}, {campaign_name}, {summary} etc. are
    left untouched so they can be filled later at actual usage time.
    """
    return prompt_template.format_map(
        _PartialFormatMap(
            language_name=tr("prompt.language_name"),
            section_major_events=tr("prompt.section.major_events"),
            section_combat=tr("prompt.section.combat"),
            section_decisions=tr("prompt.section.decisions"),
            section_mysteries=tr("prompt.section.mysteries"),
            section_active_quests=tr("prompt.section.active_quests"),
            section_clues=tr("prompt.section.clues"),
            section_completed_quests=tr("prompt.section.completed_quests"),
            quest_origin=tr("prompt.quest.origin"),
            quest_objective=tr("prompt.quest.objective"),
            quest_progress=tr("prompt.quest.progress"),
            quest_next_step=tr("prompt.quest.next_step"),
            quest_npcs=tr("prompt.quest.npcs"),
            quest_giver=tr("prompt.quest.giver"),
            quest_resolution=tr("prompt.quest.resolution"),
        )
    )


def _get_system_prompt() -> str:
    """Return the resolved system prompt for the current language."""
    return _resolve_prompt(tr("prompt.summary_system"))


def _get_user_template() -> str:
    """Return the resolved user template for the current language."""
    return tr("prompt.summary_user")


def _get_condense_prompt() -> str:
    """Return the resolved condense prompt for the current language."""
    return _resolve_prompt(tr("prompt.condense"))


# Module-level aliases used by settings.py for prompt defaults
def get_default_summary_system() -> str:
    """Return the default system prompt for the summary settings UI."""
    return _get_system_prompt()


def get_default_condense() -> str:
    """Return the default condense prompt for the summary settings UI."""
    return _get_condense_prompt()


def _call_with_retry(fn, retries=3, base_delay=15):
    """Call fn() with retry and exponential backoff on 429 rate limit."""
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            if "429" in str(e) and attempt < retries - 1:
                time.sleep(base_delay * (2**attempt))  # 15s, 30s, 60s
                continue
            raise


class SummarizerWorker(QObject):
    """Runs summarization in a QThread via Mistral chat API."""

    completed = Signal(str)  # summary HTML
    error = Signal(str)

    def __init__(self, transcript: str, quest_context: str, config: dict):
        super().__init__()
        self._transcript = transcript
        self._quest_context = quest_context
        self._config = config

    def run(self):
        """Execute summarization."""
        try:
            from mistralai import Mistral

            api_key = self._config.get("api_key", "")
            if not api_key:
                self.error.emit(tr("summarizer.error.no_api_key"))
                return

            client = Mistral(api_key=api_key)
            model = self._config.get("summary_model", "mistral-large-latest")

            transcript = self._transcript

            # Two-stage: condense first if very long
            if len(transcript) > 28000:
                transcript = self._condense(client, model, transcript)

            user_template = _get_user_template()
            user_msg = user_template.format(
                context=self._quest_context or tr("summarizer.no_context"),
                transcript=transcript,
            )

            system_prompt = self._config.get("prompt_summary_system") or _get_system_prompt()

            response = _call_with_retry(
                lambda: client.chat.complete(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_msg},
                    ],
                    temperature=0.2,
                    max_tokens=8000,
                )
            )

            summary = response.choices[0].message.content
            # Strip markdown code fences the model sometimes wraps around HTML
            summary = _strip_code_fences(summary)
            self.completed.emit(summary)

        except Exception as e:
            self.error.emit(tr("summarizer.error.generic", error=e))

    _CHUNK_SIZE = 40_000  # chars per condensation chunk

    def _condense(self, client, model: str, text: str) -> str:
        """Condense a long transcript in chunks before final summarization."""
        condense_template = self._config.get("prompt_condense") or _get_condense_prompt()
        chunks = [text[i : i + self._CHUNK_SIZE] for i in range(0, len(text), self._CHUNK_SIZE)]
        condensed_parts = []
        for chunk in chunks:
            prompt = condense_template.format(text=chunk)
            response = _call_with_retry(
                lambda: client.chat.complete(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                    max_tokens=12000,
                )
            )
            condensed_parts.append(response.choices[0].message.content)
        return "\n\n".join(condensed_parts)


def start_summarization(transcript: str, quest_context: str, config: dict) -> tuple[QThread, SummarizerWorker]:
    """Create and start a summarization worker in a new thread."""
    thread = QThread()
    worker = SummarizerWorker(transcript, quest_context, config)
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.completed.connect(thread.quit)
    worker.error.connect(thread.quit)
    return thread, worker
