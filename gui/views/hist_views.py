from PyQt6.QtWidgets import QWidget, QDialog
from gui.designer import Ui_HistorialCompras, Ui_DetallesCompra

class HistorialUi(QWidget, Ui_HistorialCompras):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class HistorialDetUi(QDialog, Ui_DetallesCompra):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    
    def mostrar_form(self):
        self.exec()