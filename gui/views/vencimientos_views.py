from PyQt6.QtWidgets import QWidget, QDialog
from gui.designer import Ui_Vencimientos, Ui_VencDetails

class VencimientosUi(QWidget, Ui_Vencimientos):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class VencDetailsUi(QWidget, Ui_VencDetails):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)