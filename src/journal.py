"""Journal — chronicle of epic session summaries."""

from datetime import datetime

from PyQt6.QtGui import QTextCursor

from .rich_editor import RichTextEditorWidget
from .utils import journal_path

_DEFAULT_JOURNAL = """\
<h1 style="color:#d4af37; text-align:center;">Journal &mdash; Icewind Dale</h1>
<hr>
<p><em>Bienvenue, aventurier. Ce journal contient la chronique de vos exploits
dans les terres glaciales d'Icewind Dale. Les recits épiques de chaque session
seront consignés ici pour la postérité.</em></p>
<hr>
"""


class JournalWidget(RichTextEditorWidget):
    """Rich-text journal for epic session summaries."""

    def __init__(self, config: dict, parent=None):
        self._config = config
        super().__init__(
            file_path=journal_path(config),
            default_html=_DEFAULT_JOURNAL,
            editor_object_name="journal_editor",
            foldable_heading_levels={2},
            fold_by_default=True,
            parent=parent,
        )

    def append_summary(self, summary_html: str):
        """Append a dated summary section at the end of the journal."""
        now = datetime.now().strftime("%d/%m/%Y")
        section = f'<hr><h2 style="color:#d4af37;">Session du {now}</h2>' f"{summary_html}<hr>"
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertHtml(section)
        self.save()
