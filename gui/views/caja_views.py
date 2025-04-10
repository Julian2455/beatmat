from PyQt6.QtWidgets import QWidget, QDialog
from gui.designer import Ui_Caja, Ui_CajaForm

class CajaUi(QWidget, Ui_Caja):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class RegisterCajaUi(QDialog, Ui_CajaForm):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
    
    def mostrar_form(self):
        self.exec()