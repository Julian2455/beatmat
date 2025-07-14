from PyQt6.QtWidgets import QDialog
from gui.designer import Ui_TrashForm

class TrashUi(QDialog, Ui_TrashForm):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
    
    def mostrar_form(self):
        self.exec()