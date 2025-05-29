from PyQt6.QtWidgets import QWidget, QDialog
from gui.designer import Ui_Gastos, Ui_GastosForm

class GastosUi(QWidget, Ui_Gastos):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class RegisterGastosUi(QDialog, Ui_GastosForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def mostrar_form(self):
        self.exec()
