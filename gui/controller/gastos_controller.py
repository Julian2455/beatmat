from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt, QObject, QDate
from PyQt6.QtGui import QAction, QColor, QPixmap, QIcon
from PyQt6 import QtCore
from models import *  
from utils import get_image
from datetime import timedelta

class GastosController(QObject):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.query=None
        self.pagina_actual = 1
        self.filas_por_pagina = 10
        self.fecha_filtro_activo = False
        self.total_gastos = Gastos.contar_gastos()
        self.total_paginas = (self.total_gastos // self.filas_por_pagina) + (1 if self.total_gastos % self.filas_por_pagina else 0)
        self.mostrar_gastos()
        self.ui.btnPreviousPage.clicked.connect(self.pagina_anterior) 
        self.ui.btnNextPage.clicked.connect(self.pagina_siguiente) 
        self.ui.btnFirstPage.clicked.connect(self.primer_pagina) 
        self.ui.btnLastPage.clicked.connect(self.ultima_pagina) 
        self.ui.btnRestaurar.setVisible(False)
        self.ui.tableGastos.verticalHeader().setVisible(False)
        self.ui.btnRestaurar.clicked.connect(self.limpiar_filtros) 
        self.ui.btnNextPage.setIcon(QIcon(get_image("sssiguiente"))) 
        self.ui.btnPreviousPage.setIcon(QIcon(get_image("anterior"))) 
        self.ui.btnFirstPage.setIcon(QIcon(get_image("anterior_1"))) 
        self.ui.btnLastPage.setIcon(QIcon(get_image("proximo_1"))) 
        self.ui.pushButton.setIcon(QIcon(get_image("dinero"))) 
        self.setupDateEdits()

    def setupDateEdits(self):
        fecha_minima_bd = Gastos.obtener_fecha_minima()
        fecha_minima = QDate.fromString((fecha_minima_bd - timedelta(days=1)).strftime("%Y-%m-%d"), "yyyy-MM-dd")
        self.ui.dateEdit.setMinimumDate(fecha_minima)
        self.ui.dateEdit.setSpecialValueText("--/--/--")
        self.ui.dateEdit.setDate(fecha_minima)
        self.fecha_filtro_activo = False
        self.ui.dateEdit.dateChanged.connect(self.on_date_changed)

    def on_date_changed(self, date):
        if date == self.ui.dateEdit.minimumDate():
            self.fecha_filtro_activo = False
            self.mostrar_gastos()
            return
        self.fecha_filtro_activo = True
        self.ui.btnRestaurar.setVisible(True)
        self.fecha_py = date.toPyDate()
        self.pagina_actual = 1 
        self.mostrar_gastos()
    
    def limpiar_filtros(self):
        self.ui.dateEdit.setDate(self.ui.dateEdit.minimumDate())
        self.fecha_filtro_activo = False
        self.fecha_py = None
        self.ui.btnRestaurar.setVisible(False)
        self.pagina_actual = 1
        self.mostrar_gastos()

    def mostrar_gastos(self):
        if self.fecha_filtro_activo:
            resultados = Gastos.buscar(self.fecha_py, page=self.pagina_actual, per_page=self.filas_por_pagina)
        else:
            resultados = Gastos.show_all(page=self.pagina_actual, per_page=self.filas_por_pagina)
        self.ui.tableGastos.setRowCount(len(resultados))
        for index, resultado in enumerate(resultados):
            gasto = resultado
            id_gasto = QTableWidgetItem(str(gasto.id))
            id_gasto.setData(Qt.ItemDataRole.UserRole, gasto.id)
            self.ui.tableGastos.setItem(index, 0, QTableWidgetItem(gasto.fecha_formateado))
            self.ui.tableGastos.setItem(index, 1, QTableWidgetItem(str(gasto.insumo)))
            gasto_formateado = f"{int(gasto.gasto):,}".replace(",", ".")
            self.ui.tableGastos.setItem(index, 2, QTableWidgetItem(gasto_formateado))
        self.actualizar_estado_paginado()

    def actualizar_estado_paginado(self):
        if self.fecha_filtro_activo:
            self.total_gastos = Gastos.contar_buscar(self.fecha_py)
        else:
            self.total_gastos = Gastos.contar_gastos()
        self.total_paginas = max(1, (self.total_gastos // self.filas_por_pagina) + (1 if self.total_gastos % self.filas_por_pagina else 0))
        if self.pagina_actual > self.total_paginas:
            self.pagina_actual = max(1, self.total_paginas)
        self.ui.labelPageInfo.setText(f"Página {self.pagina_actual} de {self.total_paginas}")
        self.ui.labelPageInfo.repaint()
        self.ui.btnPreviousPage.setEnabled(self.pagina_actual > 1)
        self.ui.btnNextPage.setEnabled(self.pagina_actual < self.total_paginas)

    def pagina_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.mostrar_gastos()

    def pagina_siguiente(self):
        self.total_gastos = Gastos.contar_gastos()
        self.total_paginas = (self.total_gastos // self.filas_por_pagina) + (1 if self.total_gastos % self.filas_por_pagina else 0)

        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.mostrar_gastos()
    
    def primer_pagina(self):
        if self.pagina_actual != 1:
            self.pagina_actual = 1
            self.mostrar_gastos()

    def ultima_pagina(self):
        if self.pagina_actual != self.total_paginas:
            self.pagina_actual = self.total_paginas
            self.mostrar_gastos()