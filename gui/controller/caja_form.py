from PyQt6.QtWidgets import QTableWidgetItem, QPushButton, QMessageBox, QMenu
from PyQt6.QtGui import QAction, QColor, QPixmap, QIcon
from PyQt6.QtCore import Qt
from models import *  
from utils import get_image

class CajaFormController:
    def __init__(self, ui, caja_controller, cliente_id=None):
        self.ui = ui
        self.caja_controller = caja_controller
        self.cliente_id = cliente_id
        self.cargar_datos()
    
    def cargar_datos(self):
        cliente=Cliente.get_by_id(self.cliente_id)
        self.ui.labelCliente.setText(f"Cliente: {cliente.nombre}")
        extintores=Extintor.disponibles() #ver si reutilizar las otras consultas
        if extintores:
            pass