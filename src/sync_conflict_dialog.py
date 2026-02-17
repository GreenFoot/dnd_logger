"""Sync conflict resolution dialog — merge local vs remote versions."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from .diff_utils import apply_inline_diff, extract_html_without_deleted
from .i18n import tr


class SyncConflictDialog(QDialog):
    """Shows local vs remote versions with a merged editor for conflict resolution."""

    def __init__(self, filename: str, local_content: str, remote_content: str, parent=None):
        super().__init__(parent)
        self._filename = filename
        self._local_content = local_content
        self._remote_content = remote_content
        self._result: str | None = None

        self.setWindowTitle(tr("conflict.title", filename=filename))
        self.setMinimumSize(900, 600)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        header = QLabel(tr("conflict.header", filename=self._filename))
        header.setWordWrap(True)
        header.setObjectName("subheading")
        layout.addWidget(header)

        # Side-by-side previews
        previews = QHBoxLayout()

        # Local version
        local_col = QVBoxLayout()
        local_label = QLabel(tr("conflict.local_label"))
        local_label.setStyleSheet("color: #6ab4d4; font-weight: bold;")
        local_col.addWidget(local_label)
        self._local_preview = QTextEdit()
        self._local_preview.setReadOnly(True)
        if self._filename.endswith(".html"):
            self._local_preview.setHtml(self._local_content)
        else:
            self._local_preview.setPlainText(self._local_content)
        local_col.addWidget(self._local_preview)
        previews.addLayout(local_col)

        # Remote version
        remote_col = QVBoxLayout()
        remote_label = QLabel(tr("conflict.remote_label"))
        remote_label.setStyleSheet("color: #d4af37; font-weight: bold;")
        remote_col.addWidget(remote_label)
        self._remote_preview = QTextEdit()
        self._remote_preview.setReadOnly(True)
        if self._filename.endswith(".html"):
            self._remote_preview.setHtml(self._remote_content)
        else:
            self._remote_preview.setPlainText(self._remote_content)
        remote_col.addWidget(self._remote_preview)
        previews.addLayout(remote_col)

        layout.addLayout(previews, stretch=1)

        # Merged editor with diff highlights
        merge_label = QLabel(tr("conflict.merge_label"))
        merge_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(merge_label)

        self._merge_editor = QTextEdit()
        self._merge_editor.setAcceptRichText(True)
        if self._filename.endswith(".html"):
            self._merge_editor.setHtml(self._remote_content)
            # Apply diff highlights: remote is "proposed", local is "current"
            local_lines = self._local_preview.toPlainText().split("\n")
            apply_inline_diff(self._merge_editor, local_lines)
        else:
            self._merge_editor.setPlainText(self._remote_content)
        layout.addWidget(self._merge_editor, stretch=1)

        # Buttons
        btn_layout = QHBoxLayout()

        btn_keep_local = QPushButton(tr("conflict.btn_keep_local"))
        btn_keep_local.setStyleSheet("color: #6ab4d4;")
        btn_keep_local.clicked.connect(self._keep_local)

        btn_keep_remote = QPushButton(tr("conflict.btn_keep_remote"))
        btn_keep_remote.setStyleSheet("color: #d4af37;")
        btn_keep_remote.clicked.connect(self._keep_remote)

        btn_save_merge = QPushButton(tr("conflict.btn_save_merge"))
        btn_save_merge.setObjectName("btn_primary")
        btn_save_merge.clicked.connect(self._save_merge)

        btn_layout.addWidget(btn_keep_local)
        btn_layout.addWidget(btn_keep_remote)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_save_merge)

        layout.addLayout(btn_layout)

    def _keep_local(self):
        self._result = self._local_content
        self.accept()

    def _keep_remote(self):
        self._result = self._remote_content
        self.accept()

    def _save_merge(self):
        if self._filename.endswith(".html"):
            self._result = extract_html_without_deleted(self._merge_editor)
        else:
            self._result = self._merge_editor.toPlainText()
        self.accept()

    def get_merged_content(self) -> str:
        """Return the resolved content."""
        return self._result or self._local_content
