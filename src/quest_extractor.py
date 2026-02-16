"""AI quest extraction from session summaries via Mistral API."""

import re

from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QTextEdit,
    QVBoxLayout,
)

from .diff_utils import apply_inline_diff, extract_html_without_deleted

_EXTRACTION_PROMPT = """\
Tu es un assistant spécialisé dans le suivi de quêtes pour une campagne \
Dungeons & Dragons ({campaign_name}).

À partir du résumé de session ci-dessous et de l'état actuel du quest log, \
génère le quest log COMPLET recompilé et enrichi avec les nouvelles \
informations de la session. Le quest log doit être un document vivant qui \
reflète l'état actuel de TOUTES les quêtes.

RÈGLE ABSOLUE — RETOURNE UNIQUEMENT LE HTML:
- Retourne UNIQUEMENT le HTML brut du quest log, RIEN d'autre.
- INTERDIT: pas d'introduction ("Voici le quest log..."), pas de conclusion, \
  pas de notes, pas de commentaires, pas de ```, pas de ---.
- Le document commence par <h1> et finit par </ul>.

Structure HTML exacte à produire (les 3 sections DOIVENT être présentes):

<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>Ce registre recense les quêtes actives, indices découverts
et mystères à élucider au cours de la campagne.</em></p>
<hr>
<h2 style="color:#6ab4d4;">Quêtes Actives</h2>
<ul>
<li><strong>Nom de la quête</strong> — Description générale de la quête.
  <ul>
  <li><em>Origine:</em> Qui a donné la quête, où et quand.</li>
  <li><em>Objectif:</em> Ce qui doit être accompli.</li>
  <li><em>Progression:</em> Ce qui a été fait jusqu'ici.</li>
  <li><em>Prochaine étape:</em> Ce qu'il reste à faire.</li>
  <li><em>PNJ impliqués:</em> Personnages liés à cette quête.</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">Indices et Mystères</h2>
<ul>
<li><strong>Mystère</strong> — Ce qu'on sait, ce qui reste à découvrir.
  <ul>
  <li>Détail ou indice découvert...</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">Quêtes Terminées</h2>
<ul>
<li><strong>Nom de la quête</strong> — Résolution et conséquences.
  <ul>
  <li><em>Mandataire:</em> Qui a donné la quête et récompense.</li>
  <li><em>Résolution:</em> Comment la quête a été résolue.</li>
  </ul>
</li>
</ul>

Règles:
- Écris en français, style concis et FACTUEL. Pas de spéculation (pas de \
  "pourrait", "semble", "suggère"). Écris uniquement ce qui est connu.
- Conserve les termes D&D en anglais (Hit Points, Saving Throw, etc.).
- Les noms propres restent tels quels.
- Utilise des listes à puces imbriquées pour les détails.
- Déplace les quêtes résolues de "Quêtes Actives" vers "Quêtes Terminées".
- PRÉSERVE TOUTES les informations existantes du quest log. Ne perds AUCUN \
  détail (mandataire, récompense, PNJ, progression) des quêtes existantes. \
  Enrichis avec les nouvelles informations SANS supprimer les anciennes.
- Ajoute les nouvelles quêtes découvertes dans "Quêtes Actives".
- Ajoute les nouveaux indices dans "Indices et Mystères". Retire un indice \
  quand le mystère est résolu (mentionne la résolution dans la quête concernée).
- Le quest log doit être un outil de référence détaillé, pas juste une liste.

État actuel du quest log:
---
{current_quests}
---

Résumé de la session:
---
{summary}
---
"""


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

    completed = pyqtSignal(str)  # quest update HTML
    error = pyqtSignal(str)

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
                self.error.emit("Clé API Mistral non configurée.")
                return

            client = Mistral(api_key=api_key)
            model = self._config.get("summary_model", "mistral-large-latest")

            prompt = _EXTRACTION_PROMPT.format(
                campaign_name=self._campaign_name or "D&D",
                current_quests=self._current_quests or "(Aucune quête enregistrée)",
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
            self.error.emit(f"Erreur d'extraction de quêtes: {e}")


class QuestProposalDialog(QDialog):
    """Editable unified-diff preview of AI-proposed quest updates.

    Shows a single view with deleted lines inline (red + strikethrough) and
    added/changed lines highlighted green.  The user can edit freely; on
    accept the deleted-marked lines are stripped and the remaining rich-text
    HTML is returned.
    """

    def __init__(self, proposed_html: str, current_html: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mise à jour des quêtes")
        self.setMinimumSize(700, 500)

        # Render current HTML through the same Qt pipeline used for proposed,
        # so line splitting is consistent for diffing.
        self._current_lines: list[str] = []
        if current_html:
            tmp = QTextEdit()
            tmp.setHtml(current_html)
            self._current_lines = tmp.toPlainText().split("\n")

        layout = QVBoxLayout(self)

        label = QLabel("Changements proposés — modifiez si nécessaire:")
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
