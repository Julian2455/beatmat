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
        self.total_clientes = Cliente.contar_clientes()
        self.total_paginas = (self.total_clientes // self.filas_por_pagina) + (1 if self.total_clientes % self.filas_por_pagina else 0)
        self.mostrar_clientes()
        self.ui.pushButton_2.clicked.connect(self.pagina_anterior) 
        self.ui.pushButton.clicked.connect(self.pagina_siguiente) 
        self.ui.pushButton_3.clicked.connect(self.primer_pagina) 
        self.ui.pushButton_4.clicked.connect(self.ultima_pagina) 
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.doubleClicked.connect(self.vencimientos_detalles) 
        self.ui.lineEdit.textChanged.connect(self.buscar_cliente)
        self.ui.pushButton.setIcon(QIcon(get_image("sssiguiente"))) 
        self.ui.pushButton_2.setIcon(QIcon(get_image("anterior"))) 
        self.ui.pushButton_3.setIcon(QIcon(get_image("anterior_1"))) 
        self.ui.pushButton_4.setIcon(QIcon(get_image("proximo_1"))) 
    def mostrar_clientes(self):
        if self.query:
            clientes=Cliente.buscar(self.query,page=self.pagina_actual, per_page=self.filas_por_pagina)
        else:
            clientes = Cliente.show_all(page=self.pagina_actual, per_page=self.filas_por_pagina)
        self.ui.tableWidget.setRowCount(len(clientes))
        for index, cliente in enumerate(clientes):
            id_cliente = QTableWidgetItem(cliente.nombre)
            id_cliente.setData(Qt.ItemDataRole.UserRole, cliente.id)
            self.ui.tableWidget.setItem(index, 0, id_cliente)
            self.ui.tableWidget.setItem(index, 1, QTableWidgetItem(cliente.direccion))
            self.ui.tableWidget.setItem(index, 2, QTableWidgetItem(str(cliente.telefono)))

        self.actualizar_estado_paginado()
    
    def obtener_id_cliente(self):
        item_seleccionado = self.ui.tableWidget.currentItem()
        if item_seleccionado:
            fila = item_seleccionado.row()
            item_con_id = self.ui.tableWidget.item(fila, 0) 
            id_cliente = item_con_id.data(Qt.ItemDataRole.UserRole)
            return id_cliente
        return None
    
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
            self.mostrar_clientes()

    def pagina_siguiente(self):
        self.total_clientes = Cliente.contar_clientes()
        self.total_paginas = (self.total_clientes // self.filas_por_pagina) + (1 if self.total_clientes % self.filas_por_pagina else 0)

        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.mostrar_clientes()
    
    def primer_pagina(self):
        if self.pagina_actual != 1:
            self.pagina_actual = 1
            self.mostrar_clientes()

    def ultima_pagina(self):
        if self.pagina_actual != self.total_paginas:
            self.pagina_actual = self.total_paginas
            self.mostrar_clientes()

    def buscar_cliente(self):
        previous_query = self.query
        self.query = self.ui.lineEdit.text()
        if previous_query != self.query:
            self.pagina_actual = 1
        self.mostrar_clientes()

    def vencimientos_detalles(self,index):
        nombre = self.ui.tableWidget.item(index.row(), 0).text()
        self.vencimientos_ui.name_client.setText(f'{nombre}')
        id_cliente=self.obtener_id_cliente()
        self.ui.hide()
        self.vencimientos_ui.show()
        self.vencimientos_ui.tableWidgetExtintores.verticalHeader().setVisible(False)
        self.vencimientos_ui.tableWidgetExtintores.setRowCount(0)
        extintores=Extintor.extintor_asociado_cliente(id_cliente)
        if extintores:
            self.vencimientos_ui.tableWidgetExtintores.setRowCount(len(extintores))
            fecha_actual=datetime.today().date()
            fecha_roja= fecha_actual + timedelta(days=10)
            fecha_verde= fecha_actual + timedelta(days=30)
            for index, resultado in enumerate(extintores):
                self.vencimientos_ui.tableWidgetExtintores.setItem(index, 0, QTableWidgetItem(str(resultado["numeracion"])))
                self.vencimientos_ui.tableWidgetExtintores.setItem(index, 1, QTableWidgetItem(str(resultado["marca"])))
                recarga = resultado["ultima_recarga"]
                if recarga:
                    vto_control_recarga=datetime.strptime(recarga.vto_control_recarga_formateado, "%d-%m-%Y").date()
                    item_control = QTableWidgetItem(recarga.vto_control_recarga_formateado)
                    if vto_control_recarga <= fecha_roja:
                        item_control.setForeground(QColor("red"))
                    elif vto_control_recarga > fecha_verde:
                        item_control.setForeground(QColor("green"))
                    else:
                        item_control.setForeground(QColor("orange"))
                    self.vencimientos_ui.tableWidgetExtintores.setItem(index, 2, item_control)
                    self.vencimientos_ui.tableWidgetExtintores.setItem(index, 3, QTableWidgetItem(str(recarga.vto_ph)))