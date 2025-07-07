
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class CreatedNewContactDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # setup UI
        uic.loadUi('ui/CreatedNewContactDialog.ui', self)
