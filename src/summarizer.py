"""Summarization via Mistral chat API with epic French fantasy style."""

from PyQt6.QtCore import QObject, QThread, pyqtSignal

_SYSTEM_PROMPT = """\
Tu es un chroniqueur épique des Royaumes Oubliés, specialisé dans la narration \
de sessions de Dungeons & Dragons. Tu écris en français avec un style héroïque \
et immersif, digne des grandes chroniques de Faerun.

Règles:
- Résume UNIQUEMENT les évènements présents dans la NOUVELLE TRANSCRIPTION. \
  Ne résume JAMAIS le contexte des sessions précédentes.
- Le contexte précédent sert uniquement de référence pour comprendre les noms, \
  lieux et intrigues déjà connus. Ne le répète pas, ne le reformule pas.
- Si la transcription ne contient aucun contenu pertinent à la campagne D&D, \
  le résumé peut être plus court pour ne pas exagéré les évènements.
- Écris en français, dans un style épique et narratif.
- Conserve TOUS les termes D&D en anglais (Hit Points, Armor Class, Saving Throw, \
  Spell Slot, Short Rest, Long Rest, etc.), ainsi que les noms des sorts.
- Les noms propres (personnages, lieux, créatures) restent tels quels.
- Formate ta réponse en HTML avec des balises <h3>, <p>, <strong>, <em>, <ul>/<li>.
- Structure le résumé en sections: Protagonistes, Évènements majeurs, \
  Combats et rencontres, Décisions importantes, Mystères et indices.
- N'inclus que les sections qui contiennent du contenu nouveau.
- Sois concis mais complet. Capture l'essence de la session.
- Ignore tout ce qui est hors sujet et qui correspondent à des discussions \
  n'ayant pas de lien avec la campagne.
"""

_USER_TEMPLATE = """\
CONTEXTE DE RÉFÉRENCE (sessions précédentes — NE PAS résumer, sert uniquement \
à comprendre les personnages, lieux et intrigues déjà établis):
---
{context}
---

NOUVELLE TRANSCRIPTION À RÉSUMER (résume UNIQUEMENT ce contenu-ci):
---
{transcript}
---

Génère un résumé épique et structuré portant EXCLUSIVEMENT sur les nouveaux \
évènements de cette transcription. Si la transcription ne contient rien de \
pertinent à la campagne, il n'est pas nécessaire d'en ajouter plus.
"""

_CONDENSE_PROMPT = """\
Tu es un assistant. Condense le texte suivant en gardant tous les éléments \
narratifs importants (personnages, lieux, évènements, décisions). \
Reduis la taille de moitié environ. Conserve les termes D&D en anglais. \
Reponds en français. Supprime en priorité ce qui est identifié comme des \
discussion ne faisant pas partie de la campagne.

Texte:
{text}
"""


class SummarizerWorker(QObject):
    """Runs summarization in a QThread via Mistral chat API."""

    completed = pyqtSignal(str)  # summary HTML
    error = pyqtSignal(str)

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
                self.error.emit("Clé API Mistral non configurée.")
                return

            client = Mistral(api_key=api_key)
            model = self._config.get("summary_model", "mistral-small-latest")

            transcript = self._transcript

            # Two-stage: condense first if very long
            if len(transcript) > 28000:
                transcript = self._condense(client, model, transcript)

            user_msg = _USER_TEMPLATE.format(
                context=self._quest_context or "(Première session — pas de contexte précédent)",
                transcript=transcript,
            )

            response = client.chat.complete(
                model=model,
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.7,
                max_tokens=4000,
            )

            summary = response.choices[0].message.content
            self.completed.emit(summary)

        except Exception as e:
            self.error.emit(f"Erreur de résumé: {e}")

    def _condense(self, client, model: str, text: str) -> str:
        """Condense a long transcript before final summarization."""
        prompt = _CONDENSE_PROMPT.format(text=text)
        response = client.chat.complete(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=8000,
        )
        return response.choices[0].message.content


def start_summarization(transcript: str, quest_context: str, config: dict) -> tuple[QThread, SummarizerWorker]:
    """Create and start a summarization worker in a new thread."""
    thread = QThread()
    worker = SummarizerWorker(transcript, quest_context, config)
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.completed.connect(thread.quit)
    worker.error.connect(thread.quit)
    return thread, worker
