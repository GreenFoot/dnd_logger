"""AI quest extraction from session summaries via Mistral API."""

from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QTextEdit, QVBoxLayout

_EXTRACTION_PROMPT = """\
Tu es un assistant spécialisé dans le suivi de quêtes pour une campagne \
Dungeons & Dragons dans Icewind Dale (Royaumes Oubliés).

À partir du resumé de session ci-dessous et de l'état actuel du quest log, \
génère le quest log COMPLET recompile et enrichi avec les nouvelles \
informations de la session. Le quest log doit etre un document vivant qui \
reflète l'état actuel de TOUTES les quêtes.

Structure HTML exacte a produire (conserve les 3 sections, même si vides):

<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; Icewind Dale</h1>
<hr>
<p><em>Ce registre recense les quêtes actives, indices découverts
et mystères a élucider dans les terres glaciales d'Icewind Dale.</em></p>
<hr>
<h2 style="color:#6ab4d4;">Quêtes Actives</h2>
<ul>
<li><strong>Nom de la quête</strong> — Description générale de la quête.
  <ul>
  <li><em>Origine:</em> Qui a donné la quête, où et quand.</li>
  <li><em>Objectif:</em> Ce qui doit être accompli.</li>
  <li><em>Progression:</em> Ce qui a été fait jusqu'ici.</li>
  <li><em>Prochaine étape:</em> Ce qu'il reste à faire.</li>
  <li><em>PNJ impliqués:</em> Personnages liés a cette quête.</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">Indices et Mystères</h2>
<ul>
<li><strong>Mystère</strong> — Ce qu'on sait, ce qui reste a découvrir.
  <ul>
  <li>Détail ou indice découvert...</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">Quêtes Terminées</h2>
<ul>
<li><strong>Nom de la quête</strong> — Résolution et conséquences.
  <ul>
  <li><em>Résolution:</em> Comment la quête a été résolue.</li>
  <li><em>Conséquences:</em> Impact sur la campagne.</li>
  </ul>
</li>
</ul>

Règles:
- Ecris en français, style concis et factuel.
- Conserve les termes D&D en anglais (Hit Points, Saving Throw, etc.).
- Les noms propres restent tels quels.
- Utilise des listes à puces imbriquées pour les détails.
- Déplace les quêtes resolues de "Quêtes Actives" vers "Quêtes Terminées".
- Enrichis les quêtes existantes avec les nouvelles informations (progression, \
indices, etc.) sans perdre les informations précédentes.
- Ajoute les nouvelles quêtes découvertes dans "Quêtes Actives".
- Ajoute les nouveaux indices dans "Indices et Mystères". Retire un indice \
quand le mystère est resolu (mentionne la resolution dans la quête concernée).
- Utilise des sous-listes imbriquées pour donner du detail sur chaque quête \
(origine, objectif, progression, prochaine étape, PNJ impliqués, etc.). \
Le quest log doit être un outil de référence détaillé, pas juste une liste.
- Génère le document HTML COMPLET du quest log, sans balise <html> ou <body>.

État actuel du quest log:
---
{current_quests}
---

Résumé de la session:
---
{summary}
---
"""


class QuestExtractorWorker(QObject):
    """Extracts quest updates from a session summary via Mistral API."""

    completed = pyqtSignal(str)  # quest update HTML
    error = pyqtSignal(str)

    def __init__(self, summary_html: str, current_quests: str, config: dict):
        super().__init__()
        self._summary = summary_html
        self._current_quests = current_quests
        self._config = config

    def run(self):
        try:
            from mistralai import Mistral

            api_key = self._config.get("api_key", "")
            if not api_key:
                self.error.emit("Cle API Mistral non configuree.")
                return

            client = Mistral(api_key=api_key)
            model = self._config.get("summary_model", "mistral-small-latest")

            prompt = _EXTRACTION_PROMPT.format(
                current_quests=self._current_quests or "(Aucune quete enregistree)",
                summary=self._summary,
            )

            response = client.chat.complete(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=3000,
            )

            result = response.choices[0].message.content
            self.completed.emit(result)

        except Exception as e:
            self.error.emit(f"Erreur d'extraction de quetes: {e}")


class QuestProposalDialog(QDialog):
    """Editable preview of AI-proposed quest updates."""

    def __init__(self, proposed_html: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mise a jour des quetes")
        self.setMinimumSize(500, 400)

        layout = QVBoxLayout(self)

        label = QLabel("Propositions de l'IA — modifiez si necessaire:")
        label.setObjectName("subheading")
        layout.addWidget(label)

        self.editor = QTextEdit()
        self.editor.setHtml(proposed_html)
        self.editor.setAcceptRichText(True)
        layout.addWidget(self.editor)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_html(self) -> str:
        """Return the (possibly edited) quest update HTML."""
        return self.editor.toHtml()


def start_quest_extraction(
    summary_html: str, current_quests: str, config: dict
) -> tuple[QThread, QuestExtractorWorker]:
    """Create a quest extraction worker in a new thread."""
    thread = QThread()
    worker = QuestExtractorWorker(summary_html, current_quests, config)
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.completed.connect(thread.quit)
    worker.error.connect(thread.quit)
    return thread, worker
