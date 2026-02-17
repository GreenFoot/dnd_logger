"""Quest Log — structured quest tracker, inherits from RichTextEditorWidget."""

from .rich_editor import RichTextEditorWidget
from .utils import active_campaign_name, quest_log_path
from .i18n import tr


def _default_quest_log_html(campaign_name: str) -> str:
    """Return the default quest log HTML template for a campaign."""
    return tr("quest_log.default_html", campaign_name=campaign_name)


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
