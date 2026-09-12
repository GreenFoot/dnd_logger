"""Dialog for ordering the audio and transcript files that belong to the same session."""

import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from .i18n import tr
from .transcriber import is_transcript_file
from .utils import format_file_size


class AudioOrderDialog(QDialog):
    """Lets the user review, reorder and trim the list of files to process.

    Files are processed back to back in the listed order, so the order is the
    chronological order of the parts within the session. Audio files are transcribed;
    files that already hold a transcript are inserted as-is at their position.
    """

    def __init__(self, paths, parent=None):
        """Initialize the dialog.

        Args:
            paths: Initial list of audio and/or transcript paths, in the order they
                were picked.
            parent: Parent widget.
        """
        super().__init__(parent)
        self.setWindowTitle(tr("session.order.title"))
        self.setMinimumSize(520, 380)

        layout = QVBoxLayout(self)

        hint = QLabel(tr("session.order.hint"))
        hint.setObjectName("subheading")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        self._list = QListWidget()
        self._list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self._list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self._list.setDefaultDropAction(Qt.DropAction.MoveAction)
        layout.addWidget(self._list, 1)

        for path in paths:
            self._add_path(path)

        btn_row = QHBoxLayout()
        self._btn_up = QPushButton(tr("session.order.btn_up"))
        self._btn_down = QPushButton(tr("session.order.btn_down"))
        self._btn_remove = QPushButton(tr("session.order.btn_remove"))
        self._btn_add = QPushButton(tr("session.order.btn_add"))
        self._btn_up.clicked.connect(lambda: self._move(-1))
        self._btn_down.clicked.connect(lambda: self._move(1))
        self._btn_remove.clicked.connect(self._remove_selected)
        self._btn_add.clicked.connect(self._add_files)
        for btn in (self._btn_up, self._btn_down, self._btn_remove, self._btn_add):
            btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self._buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self._buttons.button(QDialogButtonBox.StandardButton.Ok).setObjectName("btn_gold")
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        layout.addWidget(self._buttons)

        self._list.model().rowsInserted.connect(self._refresh)
        self._list.model().rowsRemoved.connect(self._refresh)
        self._list.model().rowsMoved.connect(self._refresh)
        self._refresh()

    def _add_path(self, path):
        """Append one file to the list, ignoring duplicates."""
        if any(self._list.item(i).data(Qt.ItemDataRole.UserRole) == path for i in range(self._list.count())):
            return
        item = QListWidgetItem(self._label(path, self._list.count()))
        item.setData(Qt.ItemDataRole.UserRole, path)
        item.setToolTip(path)
        self._list.addItem(item)

    def _add_files(self):
        """Pick extra audio or transcript files to append to the list."""
        paths, _ = QFileDialog.getOpenFileNames(
            self,
            tr("session.dialog.import_title"),
            "",
            tr("session.dialog.import_filter"),
        )
        for path in paths:
            self._add_path(path)

    def _move(self, delta):
        """Move the current item up (delta=-1) or down (delta=1)."""
        row = self._list.currentRow()
        new_row = row + delta
        if row < 0 or not 0 <= new_row < self._list.count():
            return
        item = self._list.takeItem(row)
        self._list.insertItem(new_row, item)
        self._list.setCurrentRow(new_row)

    def _remove_selected(self):
        """Drop the selected files from the list."""
        for item in self._list.selectedItems():
            self._list.takeItem(self._list.row(item))

    def _refresh(self, *_args):
        """Keep the position prefixes and the OK button in sync with the list."""
        for i in range(self._list.count()):
            item = self._list.item(i)
            path = item.data(Qt.ItemDataRole.UserRole)
            if not path:
                continue
            item.setText(self._label(path, i))
        self._buttons.button(QDialogButtonBox.StandardButton.Ok).setEnabled(self._list.count() > 0)

    @staticmethod
    def _label(path, index):
        """Build the list row text: position, file name, kind and size."""
        size = os.path.getsize(path) if os.path.exists(path) else 0
        kind = tr("session.order.type_transcript") if is_transcript_file(path) else tr("session.order.type_audio")
        return f"{index + 1}.  {os.path.basename(path)}  —  {kind}, {format_file_size(size)}"

    def ordered_paths(self) -> list[str]:
        """Return the file paths in the order chosen by the user."""
        return [self._list.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self._list.count())]
