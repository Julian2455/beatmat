from gui.controller import *
from models import *
from utils import get_image
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QPixmap
from PyQt6 import QtCore

class HistDetController(QDialog):
    def __init__(self,ui):
        super().__init__()
        self.ui = ui
        self.ui.tableDetalles.verticalHeader().setVisible(False)
        self.ui.setWindowTitle("Detalles de transacción")
        self.ui.tableDetalles.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.btnCerrar.clicked.connect(self.cerrar)
    
    def cargar_detalles(self, id_compra):
        self.ui.tableDetalles.setRowCount(0)
        venta = Caja.obtener_detalle_venta(id_compra)
        lista = venta['detalles']
        self.ui.labelFactura.setText(str(venta['id']))
        self.ui.labelCliente.setText(venta['cliente'])
        self.ui.labelFecha.setText(str(venta['fecha']))
        self.ui.labelDireccion.setText(venta['direccion'])
        self.ui.labelTelefono.setText(str(venta['telefono']))
        self.ui.labelDescripcion.setText(venta['descripcion'])
        self.ui.labelTotal.setText(str(venta['total']))
        self.ui.tableDetalles.setRowCount(len(lista))
        for index, extintor in enumerate(lista):
            item_numeracion = QTableWidgetItem(str(extintor['numeracion']))
            item_numeracion.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item_marca = QTableWidgetItem(str(extintor['marca']))
            item_marca.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item_capacidad = QTableWidgetItem(str(extintor['capacidad']))
            item_capacidad.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item_tipo = QTableWidgetItem(str(extintor['tipo']))
            item_tipo.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item_recarga = QTableWidgetItem(str(extintor['recarga']) if extintor['recarga'] is not None else "---")
            item_recarga.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item_nuevo = QTableWidgetItem(str(extintor['nuevo']) if extintor['nuevo'] is not None else "---")
            item_nuevo.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item_extras = QTableWidgetItem(str(extintor['extras']) if extintor['extras'] is not None else "---")
            item_extras.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item_total = QTableWidgetItem(str(extintor['total']) if extintor['total'] is not None else "---")
            item_total.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.tableDetalles.setItem(index, 0, item_numeracion)
            self.ui.tableDetalles.setItem(index, 1, item_marca)
            self.ui.tableDetalles.setItem(index, 2, item_capacidad)
            self.ui.tableDetalles.setItem(index, 3, item_tipo)
            self.ui.tableDetalles.setItem(index, 4, item_recarga)
            self.ui.tableDetalles.setItem(index, 5, item_nuevo)
            self.ui.tableDetalles.setItem(index, 6, item_extras)
            self.ui.tableDetalles.setItem(index, 7, item_total)
    
    def cerrar(self):
        self.ui.close()