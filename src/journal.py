"""Journal — chronicle of epic session summaries."""

import re
from datetime import datetime

from PySide6.QtGui import QTextCursor

from .i18n import tr
from .rich_editor import RichTextEditorWidget
from .utils import active_campaign_name, journal_path


def _default_journal_html(campaign_name: str) -> str:
    """Return the default journal HTML template for a campaign."""
    return tr("journal.default_html", campaign_name=campaign_name)


class JournalWidget(RichTextEditorWidget):
    """Rich-text journal for epic session summaries."""

    def __init__(self, config: dict, parent=None):
        self._config = config
        cname = active_campaign_name(config)
        super().__init__(
            file_path=journal_path(config),
            default_html=_default_journal_html(cname),
            editor_object_name="journal_editor",
            foldable_heading_levels={2},
            fold_by_default=True,
            parent=parent,
        )

    def append_summary(self, summary_html: str):
        """Append a dated summary section at the end of the journal."""
        now = datetime.now().strftime(tr("journal.date_format"))
        heading = tr("journal.session_heading", date=now)
        section = f'<hr><h2 style="color:#d4af37;">{heading}</h2>{summary_html}<hr>'
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertHtml(section)
        self.save()

    def get_session_headings(self) -> list[str]:
        """Return the text of all <h2> session headings in the journal."""
        html = self.editor.toHtml()
        return re.findall(r"<h2[^>]*>.*?(Session[^<]+)<", html, re.DOTALL | re.IGNORECASE)

    def replace_section(self, heading_text: str, summary_html: str):
        """Replace the journal section whose <h2> contains heading_text."""
        html = self.editor.toHtml()

        # Step 1: Find the <h2> tag that contains the heading text (may be wrapped in <span>)
        escaped = re.escape(heading_text)
        h2_pattern = re.compile(r"<h2[^>]*>(?:(?!</h2>).)*?" + escaped + r"(?:(?!</h2>).)*?</h2>", re.DOTALL)
        h2_match = h2_pattern.search(html)
        if not h2_match:
            return False

        # Step 2: Find the preceding <hr> if any (belongs to this section)
        section_start = h2_match.start()
        before = html[:section_start]
        hr_match = re.search(r"<hr[^>]*/?\s*>\s*$", before, re.DOTALL)
        if hr_match:
            section_start = hr_match.start()

        # Step 3: Find the end of this section (next <hr> before <h2>, or </body>)
        after_h2 = html[h2_match.end() :]
        end_pattern = re.compile(r"<hr[^>]*/?\s*>\s*(?=<h2[^>]*>)|(?=</body>)", re.DOTALL)
        end_match = end_pattern.search(after_h2)
        section_end = h2_match.end() + end_match.start() if end_match else len(html)

        # Step 4: Build replacement
        heading_tag = f'<hr><h2 style="color:#d4af37;">{heading_text}</h2>'
        replacement = f"{heading_tag}{summary_html}"
        new_html = html[:section_start] + replacement + html[section_end:]
        self.editor.setHtml(new_html)
        self.save()
        return True
