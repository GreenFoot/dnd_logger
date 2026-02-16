"""Quest Log — structured quest tracker, inherits from RichTextEditorWidget."""

from .rich_editor import RichTextEditorWidget
from .utils import active_campaign_name, quest_log_path


def _default_quest_log_html(campaign_name: str) -> str:
    """Return the default quest log HTML template for a campaign."""
    return f"""\
<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>Ce registre recense les quêtes actives, indices découverts
et mystères à élucider au cours de la campagne.</em></p>
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
        cname = active_campaign_name(config)
        super().__init__(
            file_path=quest_log_path(config),
            default_html=_default_quest_log_html(cname),
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
