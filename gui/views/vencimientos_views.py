from PyQt6.QtWidgets import QWidget, QDialog
from gui.designer import Ui_Vencimientos

class VencimientosUi(QWidget, Ui_Vencimientos):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
