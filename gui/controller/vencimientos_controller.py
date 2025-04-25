from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtGui import QAction, QIcon, QPixmap, QColor
from PyQt6.QtCore import Qt
from models import *
from utils import get_image
from datetime import datetime, timedelta

class VencimientosController:
    def __init__(self, ui):
        self.ui = ui
        self.query=None
        self.pagina_actual = 1
        self.filas_por_pagina = 10
        self.total_vencimientos = Extintor.contar_vencimientos_proximos()
        self.total_paginas = (self.total_vencimientos // self.filas_por_pagina) + (1 if self.total_vencimientos % self.filas_por_pagina else 0)
        self.mostrar_vencimientos()
        self.ui.pushButton_2.clicked.connect(self.pagina_anterior) 
        self.ui.pushButton.clicked.connect(self.pagina_siguiente) 
        self.ui.pushButton_3.clicked.connect(self.primer_pagina) 
        self.ui.pushButton_4.clicked.connect(self.ultima_pagina) 
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.pushButton.setIcon(QIcon(get_image("sssiguiente"))) 
        self.ui.pushButton_2.setIcon(QIcon(get_image("anterior"))) 
        self.ui.pushButton_3.setIcon(QIcon(get_image("anterior_1"))) 
        self.ui.pushButton_4.setIcon(QIcon(get_image("proximo_1"))) 

    def mostrar_vencimientos(self, dias=30):
        offset = (self.pagina_actual - 1) * self.filas_por_pagina
        vencimientos_proximos = Extintor.vencimientos_proximos(dias=dias, offset=offset, limit=self.filas_por_pagina)

        self.ui.tableWidget.setRowCount(0)

        if vencimientos_proximos:
            self.ui.tableWidget.setRowCount(len(vencimientos_proximos))
            for index, venc in enumerate(vencimientos_proximos):
                self.ui.tableWidget.setItem(index, 0, QTableWidgetItem(str(venc.cliente)))
                self.ui.tableWidget.setItem(index, 1, QTableWidgetItem(str(venc.numeracion)))
                self.ui.tableWidget.setItem(index, 2, QTableWidgetItem(str(venc.marca)))
                self.ui.tableWidget.setItem(index, 3, QTableWidgetItem(str(venc.vto_recarga)))
                self.ui.tableWidget.setItem(index, 4, QTableWidgetItem(str(venc.vto_ph)))
        
        self.actualizar_estado_paginado()


    def actualizar_estado_paginado(self):
        if self.query:
            self.total_clientes=Cliente.contar_buscar(self.query)
        else:
            self.total_clientes = Cliente.contar_clientes()
        self.total_paginas = (self.total_clientes // self.filas_por_pagina) + (1 if self.total_clientes % self.filas_por_pagina else 0)
        self.ui.label_7.setText(f"Página {self.pagina_actual} de {self.total_paginas}")
        self.ui.label_7.repaint()
        self.ui.pushButton_2.setEnabled(self.pagina_actual > 1)
        self.ui.pushButton.setEnabled(self.pagina_actual < self.total_paginas)

    def pagina_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.mostrar_vencimientos()

    def pagina_siguiente(self):
        self.total_clientes = Cliente.contar_clientes()
        self.total_paginas = (self.total_clientes // self.filas_por_pagina) + (1 if self.total_clientes % self.filas_por_pagina else 0)

        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.mostrar_vencimientos()
    
    def primer_pagina(self):
        if self.pagina_actual != 1:
            self.pagina_actual = 1
            self.mostrar_vencimientos()

    def ultima_pagina(self):
        if self.pagina_actual != self.total_paginas:
            self.pagina_actual = self.total_paginas
            self.mostrar_vencimientos()