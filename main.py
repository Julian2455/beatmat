from models import *
from gui.controller import *
from gui.designer import *

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
from PyQt6 import QtWidgets

class ClientUi(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class RegistroClient(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        

    def mostrar_form(self):
        self.exec()
    

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cliente_tab = ClientUi()
        self.ui.Clientes.setLayout(QtWidgets.QVBoxLayout())
        self.ui.Clientes.layout().addWidget(self.cliente_tab)
        self.client_controller = ClientController(self.cliente_tab)

        self.alta_client = RegistroClient()
        self.cliente_tab.pushButton_5.clicked.connect(self.alta_client.mostrar_form)
        
        self.form_controller = ClientFormController(self.alta_client, self.client_controller)
       
        self.setWindowTitle("LE * LO Matafuegos")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())