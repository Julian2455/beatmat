from models import *
from gui.controller import *

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from gui.designer import Ui_MainWindow 

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.client_logic = ClientController(self.ui)
        #self.product_logic = ProductLogic(self.ui)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())