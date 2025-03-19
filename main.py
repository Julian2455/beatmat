from models import *
from gui.designer import *

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Crea una instancia de la interfaz
        self.ui.setupUi(self)  # Aplica la interfaz a la ventana
        self.inicializarUI()  # Método para configuraciones adicionales

    def inicializarUI(self):
        self.setWindowTitle("LE * LO Matafuegos")  # Personaliza el título de la ventana

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()  # Muestra la ventana principal
    sys.exit(app.exec())
