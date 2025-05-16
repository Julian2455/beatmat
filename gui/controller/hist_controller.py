from PyQt6.QtWidgets import QTableWidgetItem, QMenu, QDialog, QMessageBox, QPushButton
from PyQt6.QtGui import QAction, QColor, QBrush, QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QObject, QDate
from PyQt6 import QtCore
from datetime import timedelta
from models import *  
from utils import get_image

class HistorialController(QObject): #Cuando termine asegurarme que la caja llama al metodo mostrar para que se actualice
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.pagina_actual = 1 
        self.filas_por_pagina = 10
        self.fecha_filtro_activo = False
        self.fecha_py = None
        self.cliente=None
        self.total_ventas = Caja.contar_ventas()
        self.total_paginas = (self.total_ventas // self.filas_por_pagina) + (1 if self.total_ventas % self.filas_por_pagina else 0)
        self.ui.btnPreviousPage.clicked.connect(self.pagina_anterior) 
        self.ui.btnNextPage.clicked.connect(self.pagina_siguiente) 
        self.ui.btnFirstPage.clicked.connect(self.primer_pagina) 
        self.ui.btnLastPage.clicked.connect(self.ultima_pagina) 
        self.ui.btnRestaurar.setVisible(False)
        self.ui.tableHistorialCompras.verticalHeader().setVisible(False)
        self.ui.btnRestaurar.clicked.connect(self.limpiar_filtros)
        self.ui.comboClientes.currentIndexChanged.connect(self.seleccionar_cliente)
        self.clientes_combobox()
        self.setupDateEdits()
        self.mostrar_ventas()
    
    def setupDateEdits(self):
        fecha_minima_bd = Caja.obtener_fecha_minima()
        fecha_minima = QDate.fromString((fecha_minima_bd - timedelta(days=1)).strftime("%Y-%m-%d"), "yyyy-MM-dd")
        self.ui.dateEdit.setMinimumDate(fecha_minima)
        self.ui.dateEdit.setSpecialValueText("--/--/--")
        self.ui.dateEdit.setDate(fecha_minima)
        self.fecha_filtro_activo = False
        self.ui.dateEdit.dateChanged.connect(self.on_date_changed)
    
    def on_date_changed(self, date):
        if date == self.ui.dateEdit.minimumDate():
            self.fecha_filtro_activo = False
            self.mostrar_ventas()
            return
        self.fecha_filtro_activo = True
        self.ui.btnRestaurar.setVisible(True)
        self.fecha_py = date.toPyDate()
        self.pagina_actual = 1 
        self.mostrar_ventas()
    
    def limpiar_filtros(self):
        self.ui.dateEdit.setDate(self.ui.dateEdit.minimumDate())
        self.fecha_filtro_activo = False
        self.fecha_py = None
        self.ui.comboClientes.setCurrentIndex(0)
        self.cliente = None
        self.ui.btnRestaurar.setVisible(False)
        self.pagina_actual = 1
        self.mostrar_ventas()

    def actualizar_estado_paginado(self):
        if self.fecha_filtro_activo or self.cliente:
            self.total_ventas = Caja.contar_buscar(self.cliente, self.fecha_py)
        else:
            self.total_ventas = Caja.contar_ventas()
        self.total_paginas = max(1, (self.total_ventas // self.filas_por_pagina) + (1 if self.total_ventas % self.filas_por_pagina else 0))
        if self.pagina_actual > self.total_paginas:
            self.pagina_actual = max(1, self.total_paginas)
        self.ui.labelPageInfo.setText(f"Página {self.pagina_actual} de {self.total_paginas}")
        self.ui.btnPreviousPage.setEnabled(self.pagina_actual > 1)
        self.ui.btnNextPage.setEnabled(self.pagina_actual < self.total_paginas)
        self.ui.btnFirstPage.setEnabled(self.pagina_actual > 1)
        self.ui.btnLastPage.setEnabled(self.pagina_actual < self.total_paginas)

    def pagina_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.mostrar_ventas()

    def pagina_siguiente(self):
        self.actualizar_estado_paginado()
        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.mostrar_ventas()
    
    def primer_pagina(self):
        if self.pagina_actual != 1:
            self.pagina_actual = 1
            self.mostrar_ventas()

    def ultima_pagina(self):
        if self.pagina_actual != self.total_paginas:
            self.pagina_actual = self.total_paginas
            self.mostrar_ventas()
    
    def clientes_combobox(self):
        self.ui.comboClientes.clear()
        self.ui.comboClientes.addItem("--SELECCIONAR CLIENTE--")
        clientes=Cliente.all()
        for cliente in clientes:
            self.ui.comboClientes.addItem(cliente.nombre)
            index=self.ui.comboClientes.count()-1
            self.ui.comboClientes.setItemData(index, cliente.id, QtCore.Qt.ItemDataRole.UserRole)
    
    def seleccionar_cliente(self):
        indice = self.ui.comboClientes.currentIndex()
        self.ui.tableHistorialCompras.setRowCount(0)
        if indice == 0:
            self.cliente=None
        else:
            self.ui.btnRestaurar.setVisible(True)
            self.cliente = self.ui.comboClientes.itemData(indice, QtCore.Qt.ItemDataRole.UserRole)
        self.pagina_actual = 1
        self.mostrar_ventas()

    def mostrar_ventas(self):
        self.ui.tableHistorialCompras.setRowCount(0)
        if self.fecha_filtro_activo or self.cliente:
            resultados = Caja.buscar(self.cliente, self.fecha_py, page=self.pagina_actual, per_page=self.filas_por_pagina)
        else:
            resultados = Caja.show_all(page=self.pagina_actual, per_page=self.filas_por_pagina)
        self.ui.tableHistorialCompras.setRowCount(len(resultados))
        for index, resultado in enumerate(resultados):
            venta, nombre_cliente = resultado
            id_venta = QTableWidgetItem(str(venta.id))
            id_venta.setData(Qt.ItemDataRole.UserRole, venta.id)
            self.ui.tableHistorialCompras.setItem(index, 0, id_venta)
            self.ui.tableHistorialCompras.setItem(index, 1, QTableWidgetItem(venta.fecha_formateado))
            self.ui.tableHistorialCompras.setItem(index, 2, QTableWidgetItem(nombre_cliente))
            self.ui.tableHistorialCompras.setItem(index, 3, QTableWidgetItem(str(venta.cobro)))
            self.ui.tableHistorialCompras.setItem(index, 4, QTableWidgetItem(str(venta.adeudado)))
            self.ui.tableHistorialCompras.setItem(index, 5, QTableWidgetItem(str(venta.total)))
            self.ui.tableHistorialCompras.setItem(index, 6, QTableWidgetItem(venta.descripcion or ""))
        self.actualizar_estado_paginado()