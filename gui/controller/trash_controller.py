from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox, QMenu, QWidget
from models import *
from utils import get_image
from PyQt6.QtGui import QIcon, QAction
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QObject, QLocale
from datetime import date

class TrashController(QObject):
    def __init__(self,ui,client_controller,extintor_controller):
        super().__init__()
        self.ui = ui
        self.client_controller=client_controller
        self.extintor_controller=extintor_controller
        self.ui.tableClientes.verticalHeader().setVisible(False)
        self.ui.tableClientes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.tableExtintores.verticalHeader().setVisible(False)
        self.ui.tableExtintores.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.tableClientes.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.tableClientes.customContextMenuRequested.connect(self.menu_clientes)
        self.ui.tableExtintores.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.tableExtintores.customContextMenuRequested.connect(self.menu_extintores)
        self.cargar_clientes()
        self.cargar_extintores()
    
    def cargar_clientes(self):
        self.ui.tableClientes.setRowCount(0)
        clientes=Cliente.show_deleted()
        if clientes:
            self.ui.tableClientes.setRowCount(len(clientes))
            for index, cliente in enumerate(clientes):
                id_cliente = QTableWidgetItem(cliente.nombre)
                id_cliente.setData(Qt.ItemDataRole.UserRole, cliente.id)
                self.ui.tableClientes.setItem(index, 0, id_cliente)
                self.ui.tableClientes.setItem(index, 1, QTableWidgetItem(cliente.direccion))
                self.ui.tableClientes.setItem(index, 2, QTableWidgetItem(str(cliente.telefono)))
    
    def cargar_extintores(self):
        self.ui.tableExtintores.setRowCount(0)
        extintores=Extintor.show_deleted()
        if extintores:
            self.ui.tableExtintores.setRowCount(len(extintores))
            for index, extintor in enumerate(extintores):
                id_extintor = QTableWidgetItem(str(extintor.numeracion))
                id_extintor.setData(Qt.ItemDataRole.UserRole, extintor.id)
                self.ui.tableExtintores.setItem(index, 0, id_extintor)
                self.ui.tableExtintores.setItem(index, 1, QTableWidgetItem(extintor.tipo_nombre))
                self.ui.tableExtintores.setItem(index, 2, QTableWidgetItem(extintor.marca_nombre))
                self.ui.tableExtintores.setItem(index, 3, QTableWidgetItem(extintor.capacidad_nombre))
    
    def obtener_id_tabla(self,tabla):
        item_seleccionado = tabla.currentItem()
        if item_seleccionado:
            fila_seleccionada = item_seleccionado.row()
            item_con_id = tabla.item(fila_seleccionada, 0)
            id_extintor = item_con_id.data(Qt.ItemDataRole.UserRole)
            return id_extintor
        return None
    
    def menu_desplegable(self, tabla):
        menu = QMenu(tabla)
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
        return menu

    def menu_clientes(self, pos):
        index = self.ui.tableClientes.indexAt(pos)
        if not index.isValid():
            return
        menu=self.menu_desplegable(self.ui.tableClientes)
        restaurar_action = QAction("Restaurar", self.ui.tableClientes)
        restaurar_action.triggered.connect(self.restaurar_cliente)
        menu.addAction(restaurar_action)
        menu.popup(self.ui.tableClientes.viewport().mapToGlobal(pos))
    
    def menu_extintores(self, pos):
        index = self.ui.tableExtintores.indexAt(pos)
        if not index.isValid():
            return
        menu=self.menu_desplegable(self.ui.tableExtintores)
        restaurar_action = QAction("Restaurar", self.ui.tableExtintores)
        restaurar_action.triggered.connect(self.restaurar_extintor)
        menu.addAction(restaurar_action)
        menu.popup(self.ui.tableExtintores.viewport().mapToGlobal(pos))
    
    def restaurar_cliente(self):
        id=self.obtener_id_tabla(self.ui.tableClientes)
        if id:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Restaurar Cliente")
            msg.setText(f"¿Estás seguro que quieres restaurar el cliente seleccionado?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            respuesta = msg.exec()
            if respuesta == QMessageBox.StandardButton.Yes and Cliente.restaurar(id) == True:
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Exito")
                msg.setText("Cliente restaurado correctamente.")
                msg.exec()
            else:
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Cancelación")
                msg.setText("Restauración cancelada.")
                msg.exec()
        self.cargar_clientes()
        self.ui.tableClientes.clearSelection()
        self.client_controller.mostrar_clientes() 
    
    def restaurar_extintor(self):
        id=self.obtener_id_tabla(self.ui.tableExtintores)
        if id:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Restaurar Extintor")
            msg.setText(f"¿Estás seguro que quieres restaurar el extintor seleccionado?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            respuesta = msg.exec()
            if respuesta == QMessageBox.StandardButton.Yes and Extintor.restaurar(id) == True:
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Exito")
                msg.setText("Extintor restaurado correctamente.")
                msg.exec()
            else:
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Cancelación")
                msg.setText("Restauración cancelada.")
                msg.exec()
        self.cargar_extintores()
        self.ui.tableExtintores.clearSelection() 
        self.extintor_controller.mostrar_extintores()