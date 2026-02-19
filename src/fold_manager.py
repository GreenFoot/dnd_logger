"""FoldManager — fold region scanning and state management for rich text editors."""

from dataclasses import dataclass

from PySide6.QtCore import QObject
from PySide6.QtGui import QTextDocument


@dataclass
class FoldRegion:
    """A foldable region spanning from start_block to end_block (inclusive)."""

    start: int
    end: int
    level: int
    is_folded: bool = False


class FoldManager(QObject):
    """Tracks fold regions and fold state for a QTextDocument.

    Parameters
    ----------
    document : QTextDocument
    heading_detector : callable(QTextBlock) -> int
        Returns heading level (1-3) or 0 for non-heading blocks.
    """

    # Heading levels that terminate a region at each level
    _TERMINATORS = {
        1: {1},
        2: {1, 2},
        3: {1, 2, 3},
    }

    def __init__(
        self,
        document: QTextDocument,
        heading_detector,
        foldable_heading_levels: set[int] | None = None,
        fold_by_default: bool = False,
        parent=None,
    ):
        super().__init__(parent)
        self._doc = document
        self._detect_heading = heading_detector
        self._foldable_headings = foldable_heading_levels if foldable_heading_levels is not None else {1, 2, 3}
        self._fold_by_default = fold_by_default
        self._regions: dict[int, FoldRegion] = {}
        self._dirty = True
        self._doc.contentsChanged.connect(self._mark_dirty)
        self._scan_document()

    def _mark_dirty(self):
        self._dirty = True

    def _ensure_fresh(self):
        if self._dirty:
            self._scan_document()

    def regions(self) -> dict[int, FoldRegion]:
        """Return the current fold regions, rescanning the document if needed.

        Returns:
            Mapping of start-block numbers to their FoldRegion objects.
        """
        self._ensure_fresh()
        return self._regions

    def _scan_document(self):
        """Rebuild fold regions from the document, preserving existing fold state."""
        old_folded = {start: r.is_folded for start, r in self._regions.items()}
        new_regions: dict[int, FoldRegion] = {}

        # --- Heading regions ---
        heading_blocks: list[tuple[int, int]] = []  # (block_number, level)
        block = self._doc.begin()
        while block.isValid():
            level = self._detect_heading(block)
            if level > 0:
                heading_blocks.append((block.blockNumber(), level))
            block = block.next()

        for i, (bnum, level) in enumerate(heading_blocks):
            if level not in self._foldable_headings:
                continue
            terminators = self._TERMINATORS[level]
            end_block = self._doc.blockCount() - 1  # default: end of doc
            for j in range(i + 1, len(heading_blocks)):
                next_bnum, next_level = heading_blocks[j]
                if next_level in terminators:
                    end_block = next_bnum - 1
                    break
            if end_block > bnum:
                is_folded = old_folded.get(bnum, self._fold_by_default)
                new_regions[bnum] = FoldRegion(
                    start=bnum,
                    end=end_block,
                    level=level,
                    is_folded=is_folded,
                )

        # --- Bullet list parent regions ---
        block = self._doc.begin()
        while block.isValid():
            bnum = block.blockNumber()
            text_list = block.textList()
            if text_list and bnum not in new_regions:
                indent = text_list.format().indent()
                # Scan forward for children with higher indent
                child = block.next()
                last_child = bnum
                while child.isValid():
                    cl = child.textList()
                    if cl and cl.format().indent() > indent:
                        last_child = child.blockNumber()
                    else:
                        break
                    child = child.next()
                if last_child > bnum:
                    is_folded = old_folded.get(bnum, self._fold_by_default)
                    new_regions[bnum] = FoldRegion(
                        start=bnum,
                        end=last_child,
                        level=10 + indent,
                        is_folded=is_folded,
                    )
            block = block.next()

        self._regions = new_regions
        self._dirty = False

        # Re-apply visibility for any regions that were folded
        for r in self._regions.values():
            if r.is_folded:
                self._set_block_visibility(r.start + 1, r.end, visible=False)

    def toggle_fold(self, block_num: int):
        """Toggle the fold state for the region starting at block_num."""
        self._ensure_fresh()
        region = self._regions.get(block_num)
        if region is None:
            return
        region.is_folded = not region.is_folded
        self._set_block_visibility(region.start + 1, region.end, visible=not region.is_folded)

    def fold_at(self, block_num: int):
        """Fold the region at block_num (no-op if already folded)."""
        self._ensure_fresh()
        region = self._regions.get(block_num)
        if region is None or region.is_folded:
            return
        region.is_folded = True
        self._set_block_visibility(region.start + 1, region.end, visible=False)

    def unfold_at(self, block_num: int):
        """Unfold the region at block_num (no-op if already unfolded)."""
        self._ensure_fresh()
        region = self._regions.get(block_num)
        if region is None or not region.is_folded:
            return
        region.is_folded = False
        self._set_block_visibility(region.start + 1, region.end, visible=True)

    def ensure_visible(self, block_num: int):
        """Unfold any region that hides the given block."""
        self._ensure_fresh()
        for r in self._regions.values():
            if r.is_folded and r.start < block_num <= r.end:
                r.is_folded = False
                self._set_block_visibility(r.start + 1, r.end, visible=True)

    def fold_all(self):
        """Fold every region in the document."""
        self._ensure_fresh()
        for r in self._regions.values():
            if not r.is_folded:
                r.is_folded = True
                self._set_block_visibility(r.start + 1, r.end, visible=False)

    def unfold_all(self):
        """Unfold every region in the document."""
        self._ensure_fresh()
        for r in self._regions.values():
            if r.is_folded:
                r.is_folded = False
                self._set_block_visibility(r.start + 1, r.end, visible=True)

    def save_fold_state(self) -> dict[int, bool]:
        """Return current fold states keyed by start block number."""
        self._ensure_fresh()
        return {start: r.is_folded for start, r in self._regions.items()}

    def restore_fold_state(self, state: dict[int, bool]):
        """Restore fold states after a temporary unfold."""
        self._ensure_fresh()
        for start, was_folded in state.items():
            region = self._regions.get(start)
            if region and was_folded and not region.is_folded:
                region.is_folded = True
                self._set_block_visibility(region.start + 1, region.end, visible=False)

    def _set_block_visibility(self, first: int, last: int, visible: bool):
        """Set visibility on a range of blocks and notify the document layout."""
        block = self._doc.findBlockByNumber(first)
        while block.isValid() and block.blockNumber() <= last:
            block.setVisible(visible)
            block = block.next()
        # Force layout recalculation.
        # Disconnect contentsChanged temporarily so markContentsDirty
        # does not re-dirty the fold state (causing needless re-scans).
        self._doc.contentsChanged.disconnect(self._mark_dirty)
        first_pos = self._doc.findBlockByNumber(first).position()
        last_block = self._doc.findBlockByNumber(last)
        dirty_len = last_block.position() + last_block.length() - first_pos
        self._doc.markContentsDirty(first_pos, dirty_len)
        self._doc.contentsChanged.connect(self._mark_dirty)
