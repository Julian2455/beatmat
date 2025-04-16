from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView
from models import *
from utils import get_image
from PyQt6.QtGui import QIcon
from PyQt6 import QtCore
from PyQt6.QtCore import QDate

class CajaController:
    def __init__(self,ui):
        self.ui = ui
        self.cliente=None
        self.clientes_combobox()
        self.ui.comboClientes.currentIndexChanged.connect(self.seleccionar_cliente)
        self.ui.tableExtintoresCliente.verticalHeader().setVisible(False)
        self.ui.tableExtintoresCliente.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.comboClientes.editTextChanged.connect(self.seleccionar_cliente)
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.ui.btnAgregarExtintores.setVisible(False)
    
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
        texto = self.ui.comboClientes.currentText()
        self.ui.tableExtintoresCliente.setRowCount(0)
        if indice == 0 or texto=="":
            self.cliente = None
            self.ui.btnAgregarExtintores.setVisible(False)
        else:
            self.ui.btnAgregarExtintores.setVisible(True)
            self.cliente = self.ui.comboClientes.itemData(indice, QtCore.Qt.ItemDataRole.UserRole)
            self.ui.cliente_id_actual = self.cliente
            extintores = Extintor.show_all_client(client_id=self.cliente)
            if extintores:
                self.ui.tableExtintoresCliente.setRowCount(len(extintores))
                for index, extintor in enumerate(extintores):
                    id_extintor = QTableWidgetItem(str(extintor.numeracion))
                    id_extintor.setData(QtCore.Qt.ItemDataRole.UserRole, extintor.id)
                    self.ui.tableExtintoresCliente.setItem(index, 0, id_extintor)
                    self.ui.tableExtintoresCliente.setItem(index, 1, QTableWidgetItem(extintor.marca_nombre))
                    self.ui.tableExtintoresCliente.setItem(index, 2, QTableWidgetItem(extintor.ubicacion))
                    self.ui.tableExtintoresCliente.setItem(index, 3, QTableWidgetItem(extintor.tipo_nombre))
                    self.ui.tableExtintoresCliente.setItem(index, 4, QTableWidgetItem(extintor.capacidad_nombre))
