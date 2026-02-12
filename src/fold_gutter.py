"""FoldGutterWidget — painted gutter with fold triangle indicators."""

from PyQt6.QtCore import QEvent, QPoint, Qt
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen, QPolygon
from PyQt6.QtWidgets import QTextEdit, QWidget

from .fold_manager import FoldManager

GUTTER_WIDTH = 20


class FoldGutterWidget(QWidget):
    """Narrow gutter drawn in the QTextEdit viewport margin.

    Shows gold triangles for foldable regions:
    - ▼ (down-pointing) for expanded regions
    - ▶ (right-pointing) for folded regions
    """

    def __init__(self, editor: QTextEdit, fold_manager: FoldManager, parent=None):
        super().__init__(parent or editor)
        self._editor = editor
        self._fold_mgr = fold_manager
        self._hovered_block: int | None = None

        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Track scroll and layout changes to repaint
        self._editor.verticalScrollBar().valueChanged.connect(self.update)
        self._editor.document().documentLayout().documentSizeChanged.connect(
            self._on_layout_changed
        )
        self._editor.document().contentsChanged.connect(self.update)

        # Track editor resize to reposition gutter
        self._editor.installEventFilter(self)

        # Position ourselves in the viewport
        self._reposition()

    def _reposition(self):
        """Place the gutter at the left edge of the editor viewport."""
        cr = self._editor.contentsRect()
        self.setGeometry(cr.left(), cr.top(), GUTTER_WIDTH, cr.height())

    def _on_layout_changed(self):
        self._reposition()
        self.update()

    def sizeHint(self):
        from PyQt6.QtCore import QSize
        return QSize(GUTTER_WIDTH, 0)

    # ── Painting ──────────────────────────────────────────

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background — match the editor
        painter.fillRect(event.rect(), QColor("#0d0d1e"))

        regions = self._fold_mgr.regions()
        if not regions:
            painter.end()
            return

        layout = self._editor.document().documentLayout()
        offset_y = self._editor.verticalScrollBar().value()
        viewport_top = 0
        viewport_bottom = self.height()

        gold = QColor("#c9a832")
        frost = QColor("#6ab4d4")

        for start_block, region in regions.items():
            block = self._editor.document().findBlockByNumber(start_block)
            if not block.isValid() or not block.isVisible():
                continue

            block_rect = layout.blockBoundingRect(block)
            y = int(block_rect.top() - offset_y)

            if y > viewport_bottom or y + int(block_rect.height()) < viewport_top:
                continue

            # Center the triangle vertically in the block
            cy = y + int(block_rect.height()) / 2
            is_hovered = self._hovered_block == start_block
            color = frost if is_hovered else gold

            painter.setPen(QPen(color))
            painter.setBrush(QBrush(color))

            if region.is_folded:
                # Right-pointing triangle ▶
                tri = QPolygon([
                    QPoint(6, int(cy) - 5),
                    QPoint(6, int(cy) + 5),
                    QPoint(14, int(cy)),
                ])
            else:
                # Down-pointing triangle ▼
                tri = QPolygon([
                    QPoint(5, int(cy) - 4),
                    QPoint(15, int(cy) - 4),
                    QPoint(10, int(cy) + 4),
                ])

            painter.drawPolygon(tri)

        painter.end()

    # ── Mouse interaction ─────────────────────────────────

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            block_num = self._block_at_y(event.pos().y())
            if block_num is not None and block_num in self._fold_mgr.regions():
                self._fold_mgr.toggle_fold(block_num)
                self.update()
                self._editor.viewport().update()

    def mouseMoveEvent(self, event):
        block_num = self._block_at_y(event.pos().y())
        old = self._hovered_block
        if block_num is not None and block_num in self._fold_mgr.regions():
            self._hovered_block = block_num
        else:
            self._hovered_block = None
        if old != self._hovered_block:
            self.update()

    def leaveEvent(self, event):
        if self._hovered_block is not None:
            self._hovered_block = None
            self.update()

    def event(self, event):
        """Show tooltip for folded regions."""
        if event.type() == QEvent.Type.ToolTip:
            block_num = self._block_at_y(event.pos().y())
            if block_num is not None:
                region = self._fold_mgr.regions().get(block_num)
                if region and region.is_folded:
                    count = region.end - region.start
                    from PyQt6.QtWidgets import QToolTip
                    QToolTip.showText(
                        event.globalPos(),
                        f"{count} ligne{'s' if count > 1 else ''} repliée{'s' if count > 1 else ''}",
                    )
                    return True
        return super().event(event)

    def _block_at_y(self, y: int) -> int | None:
        """Return the block number at pixel y in the gutter, or None."""
        layout = self._editor.document().documentLayout()
        offset_y = self._editor.verticalScrollBar().value()

        block = self._editor.document().begin()
        while block.isValid():
            if not block.isVisible():
                block = block.next()
                continue
            rect = layout.blockBoundingRect(block)
            block_y = int(rect.top() - offset_y)
            block_h = int(rect.height())
            if block_y <= y <= block_y + block_h:
                return block.blockNumber()
            if block_y > y:
                break
            block = block.next()
        return None

    def eventFilter(self, obj, event):
        """Reposition gutter when the editor is resized."""
        if obj is self._editor and event.type() == QEvent.Type.Resize:
            self._reposition()
        return super().eventFilter(obj, event)
