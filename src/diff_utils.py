"""Shared diff-highlighting utilities for quest proposals and sync conflicts."""

import difflib

from PySide6.QtGui import QColor, QTextBlockFormat, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import QTextEdit

COLOR_ADDED = QColor("#1a3d1a")
COLOR_DELETED_BG = QColor("#3d1a1a")
COLOR_DELETED_TEXT = QColor("#ff8888")
DELETED_STATE = 1


def filtered(lines: list[str]) -> tuple[list[str], list[int]]:
    """Normalize lines for comparison and return (filtered, index_map).

    Collapses whitespace, replaces non-breaking spaces, and drops blank
    lines so that insignificant rendering differences between the
    Qt-round-tripped current HTML and the raw proposed HTML do not produce
    false diff noise.  ``index_map[k]`` gives the original line index for
    each kept line.
    """
    out: list[str] = []
    idx_map: list[int] = []
    for i, raw in enumerate(lines):
        norm = " ".join(raw.replace("\xa0", " ").split())
        if norm:
            out.append(norm)
            idx_map.append(i)
    return out, idx_map


def apply_inline_diff(editor: QTextEdit, current_lines: list[str]) -> None:
    """Compute unified inline diff and apply highlights to the editor.

    Green background on added/changed lines; red strikethrough for deleted
    lines inserted inline.  ``current_lines`` are the *old* version's lines
    (plain text, already split by newline).
    """
    doc = editor.document()
    proposed_lines = editor.toPlainText().split("\n")

    editor.blockSignals(True)

    if not current_lines:
        # Everything is new
        for idx in range(doc.blockCount()):
            block = doc.findBlockByNumber(idx)
            if block.isValid():
                cursor = QTextCursor(block)
                fmt = block.blockFormat()
                fmt.setBackground(COLOR_ADDED)
                cursor.setBlockFormat(fmt)
        editor.moveCursor(QTextCursor.MoveOperation.Start)
        editor.blockSignals(False)
        return

    cur_filt, cur_map = filtered(current_lines)
    pro_filt, pro_map = filtered(proposed_lines)

    matcher = difflib.SequenceMatcher(None, cur_filt, pro_filt, autojunk=False)
    opcodes = matcher.get_opcodes()

    # Pass 1 — green background on added / changed proposed blocks.
    for tag, _i1, _i2, j1, j2 in opcodes:
        if tag in ("insert", "replace"):
            for k in range(j1, j2):
                block = doc.findBlockByNumber(pro_map[k])
                if block.isValid():
                    cursor = QTextCursor(block)
                    fmt = block.blockFormat()
                    fmt.setBackground(COLOR_ADDED)
                    cursor.setBlockFormat(fmt)

    # Pass 2 — collect where deleted lines should be inserted.
    insertions: list[tuple[int, list[str]]] = []
    for tag, i1, i2, j1, _j2 in opcodes:
        if tag in ("delete", "replace"):
            del_texts = [current_lines[cur_map[k]] for k in range(i1, i2)]
            if j1 < len(pro_map):
                insert_before = pro_map[j1]
            else:
                insert_before = len(proposed_lines)
            insertions.append((insert_before, del_texts))

    # Pass 3 — insert deleted lines inline, bottom-to-top.
    original_block_count = doc.blockCount()
    del_blk_fmt = QTextBlockFormat()
    del_blk_fmt.setBackground(COLOR_DELETED_BG)
    del_chr_fmt = QTextCharFormat()
    del_chr_fmt.setForeground(COLOR_DELETED_TEXT)
    del_chr_fmt.setFontStrikeOut(True)

    for proposed_idx, del_lines in reversed(insertions):
        if proposed_idx < original_block_count:
            block = doc.findBlockByNumber(proposed_idx)
            target_blk_fmt = block.blockFormat()
            cursor = QTextCursor(block)
            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
            for line in del_lines:
                cursor.insertBlock(target_blk_fmt)
                cursor.movePosition(QTextCursor.MoveOperation.PreviousBlock)
                cursor.setBlockFormat(del_blk_fmt)
                cursor.setCharFormat(del_chr_fmt)
                cursor.insertText(line)
                cursor.block().setUserState(DELETED_STATE)
                cursor.movePosition(QTextCursor.MoveOperation.NextBlock)
                cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        else:
            cursor = QTextCursor(doc)
            cursor.movePosition(QTextCursor.MoveOperation.End)
            for line in del_lines:
                cursor.insertBlock(del_blk_fmt, del_chr_fmt)
                cursor.insertText(line)
                cursor.block().setUserState(DELETED_STATE)

    editor.moveCursor(QTextCursor.MoveOperation.Start)
    editor.blockSignals(False)


def extract_html_without_deleted(editor: QTextEdit) -> str:
    """Return HTML from the editor with deleted-marked lines stripped and highlights cleared."""
    doc = editor.document()
    clean = QTextEdit()
    clean_cursor = clean.textCursor()
    first = True

    block = doc.begin()
    while block.isValid():
        if block.userState() != DELETED_STATE:
            blk_fmt = QTextBlockFormat(block.blockFormat())
            blk_fmt.clearBackground()
            if first:
                clean_cursor.setBlockFormat(blk_fmt)
                first = False
            else:
                clean_cursor.insertBlock(blk_fmt)
            src = QTextCursor(block)
            src.movePosition(
                QTextCursor.MoveOperation.EndOfBlock,
                QTextCursor.MoveMode.KeepAnchor,
            )
            if src.hasSelection():
                clean_cursor.insertFragment(src.selection())
        block = block.next()

    return clean.toHtml()
