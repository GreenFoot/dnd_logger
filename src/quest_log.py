"""Quest Log — structured quest tracker, inherits from RichTextEditorWidget."""

from .rich_editor import RichTextEditorWidget
from .utils import quest_log_path

_DEFAULT_QUEST_LOG = """\
<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; Icewind Dale</h1>
<hr>
<p><em>Ce registre recense les quêtes actives, indices découverts
et mystères à élucider dans les terres glaciales d'Icewind Dale.</em></p>
<hr>
<h2 style="color:#6ab4d4;">Quêtes Actives</h2>
<ul>
<li><em>Aucune quête enregistrée pour le moment.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Indices et Mystères</h2>
<ul>
<li><em>Aucun indice pour le moment.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Quêtes Terminées</h2>
<ul>
<li><em>Aucune quête terminée.</em></li>
</ul>
"""


class QuestLogWidget(RichTextEditorWidget):
    """Structured quest tracker with auto-save."""

    def __init__(self, config: dict, parent=None):
        self._config = config
        super().__init__(
            file_path=quest_log_path(config),
            default_html=_DEFAULT_QUEST_LOG,
            editor_object_name="quest_log_editor",
            foldable_heading_levels=set(),
            fold_by_default=True,
            parent=parent,
        )

    def replace_quest_log(self, quest_html: str):
        """Replace the entire quest log with recompiled content."""
        self.editor.setHtml(quest_html)
        self.save()

    def get_full_html(self) -> str:
        """Return the full HTML content of the quest log for recompilation."""
        return self.editor.toHtml()
