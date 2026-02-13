"""Summarization via Mistral chat API with epic French fantasy style."""

import re

from PyQt6.QtCore import QObject, QThread, pyqtSignal


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


_SYSTEM_PROMPT = """\
Tu es un chroniqueur épique des Royaumes Oubliés, specialisé dans la narration \
de sessions de Dungeons & Dragons. Tu écris en français avec un style héroïque \
et immersif, digne des grandes chroniques de Faerun.

RÈGLE ABSOLUE — FIDÉLITÉ À LA TRANSCRIPTION:
- N'INVENTE AUCUN détail qui n'est pas explicitement présent dans la transcription.
- Si une information n'est pas claire ou absente de la transcription, OMETS-LA \
  plutôt que de la deviner ou de l'inventer.
- Ne fabrique PAS de dialogue, de jets de dés, de valeurs de dégâts, de DC, \
  de noms de sorts, ou de rencontres qui ne sont pas dans la transcription.
- Chaque fait mentionné dans le résumé DOIT avoir une base dans la transcription.
- Si tu n'es pas certain d'un détail (classe d'un personnage, nom d'un sort, \
  valeur numérique), ne l'inclus pas ou signale l'incertitude.

ATTRIBUTION DES ACTIONS AUX PERSONNAGES:
- La transcription audio ne permet PAS d'identifier de manière fiable qui parle. \
  N'ATTRIBUE PAS d'actions ou de sorts à un personnage spécifique sauf si le \
  personnage est NOMMÉ EXPLICITEMENT dans le dialogue (ex: "Pryor lance un Smite").
- Si la transcription contient des marqueurs de locuteur ([Speaker 0], [Speaker 1], \
  etc.), utilise-les pour distinguer les interlocuteurs, mais NE DEVINE PAS quel \
  personnage correspond à quel locuteur.
- Quand l'attribution est incertaine, utilise des formulations impersonnelles : \
  "un aventurier", "le groupe", "l'un des héros", ou la voix passive.
- Pour les CLASSES des personnages, utilise UNIQUEMENT les informations du \
  CONTEXTE DE RÉFÉRENCE des sessions précédentes. Ne déduis JAMAIS la classe \
  d'un personnage à partir de ses actions ou sorts dans cette session.
  EXEMPLE — Transcription: "Je lance Eldritch Blast. 25, ça touche? Oui. 14 dégâts."
  BON: "Un Eldritch Blast frappe l'ennemi pour 14 dégâts."
  MAUVAIS: "Elppa lance un Eldritch Blast pour 14 dégâts." \
  (FAUX — on ne sait pas QUI parle dans la transcription audio)

DISTINCTION CRUCIALE — ACTIONS vs RÉFÉRENCES:
- Les joueurs discutent souvent d'évènements PASSÉS pendant la session : \
  récapitulatifs, rappels de lore, planification basée sur des connaissances \
  acquises lors de sessions précédentes. Ces RÉFÉRENCES ne sont PAS des \
  évènements nouveaux de cette session.
- Ne résume QUE les ACTIONS qui se déroulent activement pendant cette session : \
  exploration, combats, dialogues avec des PNJ, découvertes, décisions prises.
- Si un joueur dit "rappelle-toi, l'armure brille près des dragons" ou "la \
  dernière fois on a combattu le dragon", ce sont des RÉFÉRENCES — pas un \
  combat de dragon dans cette session.
- En cas de doute sur le fait qu'un évènement se produit MAINTENANT vs est \
  simplement MENTIONNÉ, ne l'inclus pas comme évènement de la session.
- NE TIRE PAS DE CONCLUSIONS à partir d'observations isolées. Si un objet \
  magique réagit (ex: une armure qui brille), rapporte l'observation telle \
  quelle, sans conclure sur la présence ou l'absence d'une créature ou d'un \
  danger. Les faits, pas les déductions.

Règles générales:
- Résume UNIQUEMENT les évènements présents dans la NOUVELLE TRANSCRIPTION. \
  Ne résume JAMAIS le contexte des sessions précédentes.
- Le contexte précédent sert uniquement de référence pour comprendre les noms, \
  lieux et intrigues déjà connus. Ne le répète pas, ne le reformule pas.
- Si la transcription ne contient aucun contenu pertinent à la campagne D&D, \
  le résumé peut être plus court pour ne pas exagérer les évènements.
- Écris en français, dans un style épique et narratif, mais JAMAIS au prix \
  de l'exactitude. Le style sert la narration, pas l'invention.
- Conserve TOUS les termes D&D en anglais (Hit Points, Armor Class, Saving Throw, \
  Spell Slot, Short Rest, Long Rest, etc.), ainsi que les noms des sorts.
- Les noms propres (personnages, lieux, créatures) restent tels quels.
- Ignore les discussions hors-sujet sans lien avec la campagne.

Qualité de la transcription:
- La transcription provient d'un modèle speech-to-text qui peut produire des \
  artefacts : phrases répétées en boucle, texte incohérent, mots inventés. \
  Ignore complètement ces passages parasites et concentre-toi uniquement sur \
  le contenu narratif pertinent à la session D&D.
- ATTENTION : certains passages peuvent sembler narratifs mais être des artefacts. \
  Si un passage ne s'intègre pas logiquement avec le reste de la session, \
  c'est probablement un artefact — ignore-le.

Format et structure:
- Formate ta réponse en HTML avec des balises <h3>, <p>, <strong>, <em>, <ul>/<li>.
- Retourne UNIQUEMENT le HTML brut.
- INTERDIT: pas de ```, pas de ---, pas de séparateurs, pas de commentaires méta.
- N'inclus que les sections qui contiennent du contenu nouveau.
- MISE EN FORME : listes à puces SIMPLES (un seul niveau de <ul>/<li>). \
  N'imbrique JAMAIS de sous-listes. Garde chaque point concis sur une seule ligne.
- Structure le résumé avec EXACTEMENT ces sections dans cet ordre. \
  Chaque section commence par un <h3> suivi du contenu. \
  Tu DOIS inclure TOUTES les sections qui ont du contenu pertinent.

<h3>Évènements majeurs</h3>
Récit narratif et chronologique des évènements de la session. \
Décris les lieux découverts, les rencontres avec les PNJ, et les \
découvertes. Utilise un ton immersif et descriptif. \
C'est la section principale et la plus longue du résumé. \
Rapporte les OBSERVATIONS telles quelles, sans en tirer de conclusions \
(ex: si une armure brille, ne conclus PAS qu'un dragon est proche).

<h3>Combats</h3>
Pour CHAQUE combat de la session, écris un COURT PARAGRAPHE NARRATIF \
(3-5 phrases) décrivant : les ennemis affrontés, les moments marquants \
(sorts puissants, coups critiques, dangers), et l'issue du combat. \
N'énumère PAS chaque tour ou jet individuellement. \
RAPPEL: n'attribue PAS les sorts ou attaques à un personnage nommé \
sauf si le nom est EXPLICITEMENT dit dans la transcription. Préfère \
la voix passive : "un Eldritch Blast frappe", "un Divine Smite terrasse". \
Si aucun combat n'a eu lieu, OMETS cette section.

<h3>Décisions et découvertes</h3>
SEULEMENT les 3-5 faits les plus impactants pour la CAMPAGNE : \
objets magiques identifiés (propriétés ET malédictions en une phrase), \
choix stratégiques majeurs, informations cruciales obtenues. \
Format: liste PLATE <ul>/<li>, UNE ligne par élément, ZÉRO sous-liste. \
EXEMPLE de format correct: \
<li><strong>Hache maudite</strong> — +1 attaque/dégâts et +1 PV/niveau, \
mais impossible à abandonner, berserk sur Wisdom Save raté, désavantage \
avec d'autres armes.</li>

<h3>Mystères et indices</h3>
SEULEMENT si un élément de cette session éclaire un mystère DÉJÀ CONNU \
du CONTEXTE DE RÉFÉRENCE (quête du codex, menace d'Auril, etc.). \
Maximum 2-3 éléments. \
Format: liste simple <ul>/<li>, phrase DÉCLARATIVE factuelle. \
INTERDIT: questions rhétoriques, hypothèses, spéculations, verbes comme \
"suggère", "semble", "pourrait", "indique que". \
EXEMPLE — BON: "Le serment de Vassaviken confirme que Grimskal fut le \
fief d'une reine des géants des glaces menant des campagnes de pillage." \
MAUVAIS: "La régénération de la créature suggère une magie liée à Auril." \
(FAUX — c'est une spéculation, pas un fait observé dans la transcription) \
Si rien n'éclaire les intrigues connues, OMETS cette section entièrement.
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
évènements de cette transcription. Couvre TOUS les évènements significatifs \
de la transcription dans l'ordre chronologique — ne te concentre pas sur \
une seule scène au détriment des autres. Si la transcription ne contient \
rien de pertinent à la campagne, il n'est pas nécessaire d'en ajouter plus.
"""

_CONDENSE_PROMPT = """\
Tu es un assistant spécialisé dans le traitement de transcriptions de sessions \
de Dungeons & Dragons.

La transcription provient d'un modèle speech-to-text qui produit de nombreux \
artefacts : phrases répétées en boucle, texte incohérent, mots inventés, \
passages sans rapport avec la session D&D. Ignore complètement ces passages \
parasites.

Condense le texte en gardant UNIQUEMENT les éléments narratifs pertinents à \
la campagne D&D. Conserve les termes D&D en anglais. Réponds en français.

Éléments à PRÉSERVER ABSOLUMENT:
- Noms des personnages, PNJ et créatures rencontrées
- Lieux découverts avec leurs descriptions physiques
- DIALOGUES AVEC LES PNJ : conserve TOUT ce qu'un PNJ révèle (informations, \
  directions, avertissements, noms mentionnés, lore). C'est critique — les \
  informations données par les PNJ sont souvent les plus importantes de la session.
- Combats : ennemis, valeurs numériques (jets, dégâts, AC, DC, HP, initiative)
- Objets magiques : propriétés complètes ET malédictions
- Actions RATÉES et leurs conséquences (explosions, dégâts subis, échecs)
- Décisions prises par le groupe et leurs résultats immédiats

DISTINCTION ACTIONS vs RÉFÉRENCES:
- Les joueurs discutent souvent d'évènements PASSÉS : récapitulatifs de sessions \
  précédentes, rappels de lore, planification. Ces discussions ne sont PAS des \
  évènements de la session en cours.
- Ne retiens QUE les ACTIONS qui se déroulent activement : exploration de lieux, \
  combats en cours, dialogues avec des PNJ rencontrés, découvertes faites, \
  décisions prises.
- Si un joueur MENTIONNE un évènement passé (ex: "rappelle-toi le dragon", \
  "la dernière fois on a trouvé..."), c'est une RÉFÉRENCE — ignore-la. \
  Seuls les évènements qui SE PRODUISENT pendant la session comptent.
- Ne tire PAS de conclusions à partir d'observations ou de discussions \
  entre joueurs. Rapporte UNIQUEMENT les faits bruts, jamais les déductions.

IMPORTANT:
- Retourne UNIQUEMENT les faits narratifs bruts, dans l'ordre chronologique.
- N'ajoute PAS de méta-commentaires, conclusions, résumés, suggestions, \
  "points clés à retenir", "prochaines étapes" ou "questions en suspens".
- N'ajoute PAS de séparateurs (---), de titres de section formatés, ni de \
  commentaires sur la qualité de la transcription.
- Préserve les NOMS EXACTS des personnages tels qu'entendus (Elppa, Pryor, \
  Sabor, Nozama, Vélin, etc.) sans les modifier ni ajouter de points \
  d'interrogation.
- Même si le texte contient beaucoup de bruit, extrais TOUT fragment de \
  contenu D&D qui s'y trouve, aussi petit soit-il. Ne retourne une réponse \
  vide que si le texte est à 100% des artefacts sans aucune phrase cohérente \
  liée au jeu.

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
            model = self._config.get("summary_model", "mistral-large-latest")

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
                temperature=0.2,
                max_tokens=8000,
            )

            summary = response.choices[0].message.content
            # Strip markdown code fences the model sometimes wraps around HTML
            summary = _strip_code_fences(summary)
            self.completed.emit(summary)

        except Exception as e:
            self.error.emit(f"Erreur de résumé: {e}")

    _CHUNK_SIZE = 40_000  # chars per condensation chunk

    def _condense(self, client, model: str, text: str) -> str:
        """Condense a long transcript in chunks before final summarization."""
        chunks = [text[i : i + self._CHUNK_SIZE] for i in range(0, len(text), self._CHUNK_SIZE)]
        condensed_parts = []
        for chunk in chunks:
            prompt = _CONDENSE_PROMPT.format(text=chunk)
            response = client.chat.complete(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=12000,
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
