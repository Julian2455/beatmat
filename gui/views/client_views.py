from PyQt6.QtWidgets import QWidget, QDialog
from gui.designer import Ui_Client, Ui_ExtintorClientsDetails, Ui_ClientForm

class ClientUi(QWidget, Ui_Client):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class ExtintorClientsDetailsUi(QWidget, Ui_ExtintorClientsDetails):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class RegisterClientUi(QDialog, Ui_ClientForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def mostrar_form(self):
        self.exec()