from PyQt6.QtWidgets import QWidget, QDialog
from gui.designer import Ui_Caja, Ui_AgregarExtintores, Ui_FormPrecios

class CajaUi(QWidget, Ui_Caja):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class AgregarExtintorUi(QDialog, Ui_AgregarExtintores):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
    
    def mostrar_form(self, cliente_id=None):
        self.cliente_id = cliente_id
        self.exec()

class PreciosUi(QDialog, Ui_FormPrecios):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
    
    def mostrar_form(self):
        self.exec()