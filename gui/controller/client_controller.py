from PyQt6.QtWidgets import QTableWidgetItem, QPushButton, QMessageBox, QMenu
from PyQt6.QtGui import QAction, QColor
from PyQt6.QtCore import Qt
from models import *  
from datetime import datetime, timedelta

class ClientController:
    def __init__(self, ui):
        self.ui = ui
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
        self.ui.tableWidget.doubleClicked.connect(self.extintores_clientes)
        self.ui.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.tableWidget.customContextMenuRequested.connect(self.mostrar_menu_contextual)
        self.edit_form_cli = None

    def mostrar_clientes(self):
        clientes = Cliente.show_all(page=self.pagina_actual, per_page=self.filas_por_pagina)
        self.ui.tableWidget.setRowCount(len(clientes))
        for index, cliente in enumerate(clientes):
            id_cliente = QTableWidgetItem(cliente.nombre)
            id_cliente.setData(Qt.ItemDataRole.UserRole, cliente.id)
            self.ui.tableWidget.setItem(index, 0, id_cliente)
            self.ui.tableWidget.setItem(index, 1, QTableWidgetItem(cliente.direccion))

        self.actualizar_estado_paginado()

    def mostrar_menu_contextual(self, pos):
        index = self.ui.tableWidget.indexAt(pos)
        if not index.isValid():
            return
        menu = QMenu(self.ui.tableWidget)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #CCCCCC;
            }
            QMenu::item {
                padding: 5px 15px;
                background-color: white;
            }
            QMenu::item:selected {
                background-color: #E0E0E0;
                color: black;
            }
        """)
        editar_action = QAction("Editar", self.ui.tableWidget)
        eliminar_action = QAction("Eliminar", self.ui.tableWidget)
        editar_action.triggered.connect(self.editar_cliente)
        eliminar_action.triggered.connect(self.eliminar_cliente)
        menu.addAction(editar_action)
        menu.addAction(eliminar_action)
        menu.exec(self.ui.tableWidget.viewport().mapToGlobal(pos))
    
    def set_edit_form_cli(self, edit_form_cli):
        self.edit_form_cli = edit_form_cli
    
    def obtener_id_cliente(self):
        item_seleccionado = self.ui.tableWidget.currentItem()
        if item_seleccionado:
            fila = item_seleccionado.row()
            item_con_id = self.ui.tableWidget.item(fila, 0) 
            id_cliente = item_con_id.data(Qt.ItemDataRole.UserRole)
            return id_cliente
        return None

    def editar_cliente(self):
        id_cliente = self.obtener_id_cliente()
        if id_cliente and self.edit_form_cli:
            self.edit_form_cli.setWindowTitle("Editar Cliente")
            cliente = Cliente.get_by_id(id_cliente)
            if cliente:
                self.edit_form_cli.label_2.setText("EDITAR CLIENTE")
                self.edit_form_cli.lineEdit.setText(cliente.nombre)
                self.edit_form_cli.lineEdit_2.setText(cliente.direccion)
                self.edit_client_controller.cliente_id = id_cliente
                self.edit_form_cli.mostrar_form()
    
    def eliminar_cliente(self):
        id_cliente = self.obtener_id_cliente()
        if id_cliente: #Aca tiene que ir la logica para eliminar y el mensaje, pero hay que hacerlo despues, por la relacion con las otras tablas
            print(f"Eliminar : {id_cliente}")

    def actualizar_estado_paginado(self):
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

    def extintores_clientes(self,index):
        nombre = self.ui.tableWidget.item(index.row(), 0).text()
        self.asociacion_ui.labelExtintores.setText(f'Extintores asociados a {nombre}')
        id_cliente=self.obtener_id_cliente()
        self.ui.hide()
        self.asociacion_ui.show()
        self.asociacion_ui.tableWidgetExtintores.verticalHeader().setVisible(False)
        self.asociacion_ui.tableWidgetExtintores.setRowCount(0)
        extintores=Extintor.extintor_asociado_cliente(id_cliente)
        if extintores:
            self.asociacion_ui.tableWidgetExtintores.setRowCount(len(extintores))
            fecha_actual=datetime.today().date()
            fecha_roja= fecha_actual + timedelta(days=10)
            fecha_verde= fecha_actual + timedelta(days=30)
            for index, (extintor, recarga) in enumerate(extintores):
                self.asociacion_ui.tableWidgetExtintores.setItem(index, 0, QTableWidgetItem(str(extintor.numeracion)))
                self.asociacion_ui.tableWidgetExtintores.setItem(index, 1, QTableWidgetItem(str(extintor.marca)))
                vto_control_recarga=datetime.strptime(recarga.vto_control_recarga_formateado, "%d-%m-%Y").date()
                item_control = QTableWidgetItem(recarga.vto_control_recarga_formateado)
                if vto_control_recarga <= fecha_roja:
                    item_control.setForeground(QColor("red"))
                elif vto_control_recarga > fecha_verde:
                    item_control.setForeground(QColor("green"))
                else:
                    item_control.setForeground(QColor("orange"))
                self.asociacion_ui.tableWidgetExtintores.setItem(index, 2, item_control)
                self.asociacion_ui.tableWidgetExtintores.setItem(index, 3, QTableWidgetItem(str(recarga.vto_ph)))

