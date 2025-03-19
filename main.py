from models import *
from gui.designer import *

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
from gui.designer.abmclientes import Ui_Dialog

class AbmClientes(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Crea una instancia de la interfaz
        self.ui.setupUi(self)  # Aplica la interfaz a la ventana
        self.inicializarUI()  # Método para configuraciones adicionales

        #Con esto se conecta el boton del modulo clientes a la ventana donde estan todos
        self.ui.botonclients.clicked.connect(self.abrir_ventana_clientes)

    def abrir_ventana_clientes(self):
        self.ventana_clientes = AbmClientes()
        self.ventana_clientes.exec()

    def inicializarUI(self):
        self.setWindowTitle("LE * LO Matafuegos")  # Personaliza el título de la ventana

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()  # Muestra la ventana principal
    sys.exit(app.exec())
