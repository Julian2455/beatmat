from PyQt6.QtWidgets import QWidget
from gui.designer import Ui_HistorialCompras

class HistorialUi(QWidget, Ui_HistorialCompras):
    def __init__(self):
        super().__init__()
        self.setupUi(self)