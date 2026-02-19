"""Themed dialog helpers — instance-based so they inherit the app's QSS."""

from PySide6.QtWidgets import QComboBox, QDialog, QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout

from .i18n import tr

# ── Message boxes ────────────────────────────────────────


def information(parent, title, text):
    """Show a themed information message box.

    Args:
        parent: Parent widget for the dialog.
        title: Window title.
        text: Message body text.
    """
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Icon.Information)
    box.setWindowTitle(title)
    box.setText(text)
    box.exec()


def warning(parent, title, text):
    """Show a themed warning message box.

    Args:
        parent: Parent widget for the dialog.
        title: Window title.
        text: Message body text.
    """
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Icon.Warning)
    box.setWindowTitle(title)
    box.setText(text)
    box.exec()


def critical(parent, title, text):
    """Show a themed critical error message box.

    Args:
        parent: Parent widget for the dialog.
        title: Window title.
        text: Message body text.
    """
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Icon.Critical)
    box.setWindowTitle(title)
    box.setText(text)
    box.exec()


def question(parent, title, text) -> bool:
    """Show a themed yes/no question dialog.

    Args:
        parent: Parent widget for the dialog.
        title: Window title.
        text: Question body text.

    Returns:
        True if the user clicked Yes, False otherwise.
    """
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Icon.Question)
    box.setWindowTitle(title)
    box.setText(text)
    box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    return box.exec() == QMessageBox.StandardButton.Yes


# ── Item picker (replaces QInputDialog.getItem) ─────────


def get_item(parent, title, label, items, current=0, editable=False):
    """Themed replacement for QInputDialog.getItem.

    Args:
        parent: Parent widget for the dialog.
        title: Window title.
        label: Descriptive label above the combo box.
        items: List of selectable string items.
        current: Index of the initially selected item.
        editable: Whether the combo box allows free-text input.

    Returns:
        Tuple of (selected_text, accepted) where accepted is True if OK was clicked.
    """
    dlg = QDialog(parent)
    dlg.setWindowTitle(title)
    dlg.setMinimumWidth(320)

    layout = QVBoxLayout(dlg)
    layout.setSpacing(12)
    layout.setContentsMargins(20, 20, 20, 16)

    lbl = QLabel(label)
    lbl.setWordWrap(True)
    layout.addWidget(lbl)

    combo = QComboBox()
    combo.addItems(items)
    if 0 <= current < len(items):
        combo.setCurrentIndex(current)
    combo.setEditable(editable)
    layout.addWidget(combo)

    btn_row = QHBoxLayout()
    btn_row.addStretch()
    btn_cancel = QPushButton(tr("dialog.btn_cancel"))
    btn_ok = QPushButton(tr("dialog.btn_ok"))
    btn_ok.setObjectName("btn_primary")
    btn_row.addWidget(btn_cancel)
    btn_row.addWidget(btn_ok)
    layout.addLayout(btn_row)

    btn_cancel.clicked.connect(dlg.reject)
    btn_ok.clicked.connect(dlg.accept)

    ok = dlg.exec() == QDialog.DialogCode.Accepted
    return (combo.currentText(), ok)
