"""AI quest extraction from session summaries via Mistral API."""

import difflib
import re

from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QTextBlockFormat, QTextCharFormat, QTextCursor
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QTextEdit,
    QVBoxLayout,
)

_EXTRACTION_PROMPT = """\
Tu es un assistant spécialisé dans le suivi de quêtes pour une campagne \
Dungeons & Dragons dans Icewind Dale (Royaumes Oubliés).

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

<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; Icewind Dale</h1>
<hr>
<p><em>Ce registre recense les quêtes actives, indices découverts
et mystères à élucider dans les terres glaciales d'Icewind Dale.</em></p>
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
                self.error.emit("Clé API Mistral non configurée.")
                return

            client = Mistral(api_key=api_key)
            model = self._config.get("summary_model", "mistral-large-latest")

            prompt = _EXTRACTION_PROMPT.format(
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


_COLOR_ADDED = QColor("#1a3d1a")
_COLOR_DELETED_BG = QColor("#3d1a1a")
_COLOR_DELETED_TEXT = QColor("#ff8888")
_DELETED_STATE = 1


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

        self._apply_diff_highlights()

    # ------------------------------------------------------------------
    # Diff highlighting
    # ------------------------------------------------------------------

    @staticmethod
    def _filtered(lines: list[str]) -> tuple[list[str], list[int]]:
        """Normalize lines for comparison and return (filtered, index_map).

        Collapses whitespace, replaces non-breaking spaces, and drops blank
        lines so that insignificant rendering differences between the
        Qt-round-tripped current HTML and the raw Mistral-proposed HTML do
        not produce false diff noise.  ``index_map[k]`` gives the original
        line index for each kept line.
        """
        out: list[str] = []
        idx_map: list[int] = []
        for i, raw in enumerate(lines):
            norm = " ".join(raw.replace("\xa0", " ").split())
            if norm:
                out.append(norm)
                idx_map.append(i)
        return out, idx_map

    def _apply_diff_highlights(self):
        """Compute diff and insert inline highlights (green=added, red=deleted)."""
        doc = self.editor.document()
        proposed_lines = self.editor.toPlainText().split("\n")
        current_lines = self._current_lines

        self.editor.blockSignals(True)

        if not current_lines:
            # First-ever quest log — everything is new.
            for idx in range(doc.blockCount()):
                block = doc.findBlockByNumber(idx)
                if block.isValid():
                    cursor = QTextCursor(block)
                    fmt = block.blockFormat()
                    fmt.setBackground(_COLOR_ADDED)
                    cursor.setBlockFormat(fmt)
            self.editor.moveCursor(QTextCursor.MoveOperation.Start)
            self.editor.blockSignals(False)
            return

        # Compare *normalized, non-blank* lines so whitespace / nbsp
        # differences between the two HTML renderings don't cause the
        # entire document to show as replaced.
        cur_filt, cur_map = self._filtered(current_lines)
        pro_filt, pro_map = self._filtered(proposed_lines)

        matcher = difflib.SequenceMatcher(
            None, cur_filt, pro_filt, autojunk=False
        )
        opcodes = matcher.get_opcodes()

        # Pass 1 — green background on added / changed proposed blocks.
        for tag, _i1, _i2, j1, j2 in opcodes:
            if tag in ("insert", "replace"):
                for k in range(j1, j2):
                    block = doc.findBlockByNumber(pro_map[k])
                    if block.isValid():
                        cursor = QTextCursor(block)
                        fmt = block.blockFormat()
                        fmt.setBackground(_COLOR_ADDED)
                        cursor.setBlockFormat(fmt)

        # Pass 2 — collect where deleted lines should be inserted.
        # Each entry is (proposed_block_number, [original_line_texts]).
        insertions: list[tuple[int, list[str]]] = []
        for tag, i1, i2, j1, _j2 in opcodes:
            if tag in ("delete", "replace"):
                del_texts = [current_lines[cur_map[k]] for k in range(i1, i2)]
                if j1 < len(pro_map):
                    insert_before = pro_map[j1]
                else:
                    insert_before = len(proposed_lines)  # append at end
                insertions.append((insert_before, del_texts))

        # Pass 3 — insert deleted lines inline, processing bottom-to-top so
        # that earlier block numbers remain stable.
        original_block_count = doc.blockCount()
        del_blk_fmt = QTextBlockFormat()
        del_blk_fmt.setBackground(_COLOR_DELETED_BG)
        del_chr_fmt = QTextCharFormat()
        del_chr_fmt.setForeground(_COLOR_DELETED_TEXT)
        del_chr_fmt.setFontStrikeOut(True)

        for proposed_idx, del_lines in reversed(insertions):
            if proposed_idx < original_block_count:
                # Insert each deleted line *before* the target block.
                block = doc.findBlockByNumber(proposed_idx)
                # Save the original block format so insertBlock() can
                # hand it to the displaced content block, preserving
                # heading level, list membership, alignment, etc.
                target_blk_fmt = block.blockFormat()
                cursor = QTextCursor(block)
                cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
                for line in del_lines:
                    # insertBlock(fmt) at start-of-block pushes existing
                    # content to the next block with *fmt*, keeping its
                    # structural formatting intact.
                    cursor.insertBlock(target_blk_fmt)
                    cursor.movePosition(
                        QTextCursor.MoveOperation.PreviousBlock
                    )
                    cursor.setBlockFormat(del_blk_fmt)
                    cursor.setCharFormat(del_chr_fmt)
                    cursor.insertText(line)
                    cursor.block().setUserState(_DELETED_STATE)
                    # Return to the (shifted) target block for the next line.
                    cursor.movePosition(QTextCursor.MoveOperation.NextBlock)
                    cursor.movePosition(
                        QTextCursor.MoveOperation.StartOfBlock
                    )
            else:
                # Deletion at the very end — append after last block.
                cursor = QTextCursor(doc)
                cursor.movePosition(QTextCursor.MoveOperation.End)
                for line in del_lines:
                    cursor.insertBlock(del_blk_fmt, del_chr_fmt)
                    cursor.insertText(line)
                    cursor.block().setUserState(_DELETED_STATE)

        self.editor.moveCursor(QTextCursor.MoveOperation.Start)
        self.editor.blockSignals(False)

    # ------------------------------------------------------------------
    # HTML extraction
    # ------------------------------------------------------------------

    def get_html(self) -> str:
        """Return quest HTML with deleted-marked lines stripped and highlights cleared."""
        doc = self.editor.document()
        clean = QTextEdit()
        clean_cursor = clean.textCursor()
        first = True

        block = doc.begin()
        while block.isValid():
            if block.userState() != _DELETED_STATE:
                blk_fmt = QTextBlockFormat(block.blockFormat())
                blk_fmt.clearBackground()
                if first:
                    clean_cursor.setBlockFormat(blk_fmt)
                    first = False
                else:
                    clean_cursor.insertBlock(blk_fmt)
                # Copy block content preserving character formatting.
                src = QTextCursor(block)
                src.movePosition(
                    QTextCursor.MoveOperation.EndOfBlock,
                    QTextCursor.MoveMode.KeepAnchor,
                )
                if src.hasSelection():
                    clean_cursor.insertFragment(src.selection())
            block = block.next()

        return clean.toHtml()


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
