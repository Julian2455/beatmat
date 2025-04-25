from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QMenu, QMessageBox, QCheckBox, QLineEdit
from models import *
from utils import get_image
from PyQt6.QtGui import QIcon, QAction
from PyQt6 import QtCore
from PyQt6.QtCore import QDate, Qt, QObject

class CajaController(QObject):
    def __init__(self,ui):
        super().__init__()
        self.ui = ui
        self.cliente=None
        self.clientes_combobox()
        self.ui.comboClientes.currentIndexChanged.connect(self.seleccionar_cliente)
        self.ui.tableExtintoresCliente.verticalHeader().setVisible(False)
        self.ui.tableDetalleFactura.verticalHeader().setVisible(False)
        self.ui.tableExtintoresCliente.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.comboClientes.editTextChanged.connect(self.seleccionar_cliente)
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.ui.btnAgregarExtintores.setVisible(False)
        self.ui.tableExtintoresCliente.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.tableExtintoresCliente.customContextMenuRequested.connect(self.mostrar_menu_contextual)
        self.selected_extintores={}
    
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
        self.seleccionar_valores()

    def mostrar_menu_contextual(self, pos):
        index = self.ui.tableExtintoresCliente.indexAt(pos)
        if not index.isValid():
            return
        menu = QMenu(self.ui.tableExtintoresCliente)
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
        eliminar_action = QAction("Eliminar", self.ui.tableExtintoresCliente)
        eliminar_action.triggered.connect(self.eliminar_extintor)
        menu.addAction(eliminar_action)
        menu.exec(self.ui.tableExtintoresCliente.viewport().mapToGlobal(pos))
    
    def obtener_id_extintor(self):
        item_seleccionado = self.ui.tableExtintoresCliente.currentItem()
        if item_seleccionado:
            fila = item_seleccionado.row()
            item_con_id = self.ui.tableExtintoresCliente.item(fila, 0) 
            id_extintor = item_con_id.data(Qt.ItemDataRole.UserRole)
            return id_extintor
        return None

    def eliminar_extintor(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Confirmar eliminación")
        msg.setText("¿Estás seguro de que deseas eliminar este extintor de la lista?")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg.setDefaultButton(QMessageBox.StandardButton.Cancel)
        respuesta = msg.exec()
        if respuesta == QMessageBox.StandardButton.Ok:
            id_extintor = self.obtener_id_extintor()
            Extintor.liberar_extintor(id_extintor)
            self.seleccionar_cliente()
        else:
            pass
    
    def seleccionar_valores(self):
        if self.cliente:
            extintores = Extintor.show_all_client_pay(client_id=self.cliente)
            if extintores:
                self.ui.tableDetalleFactura.setRowCount(len(extintores))
                for index, extintor in enumerate(extintores):
                    id_extintor = QTableWidgetItem(str(extintor.numeracion))
                    id_extintor.setData(QtCore.Qt.ItemDataRole.UserRole, extintor.id)
                    checkbox = QCheckBox()
                    checkbox.setProperty("extintor_id", extintor.id)
                    checkbox.setStyleSheet("QCheckBox { margin-left: 30px; }")
                    checkbox.stateChanged.connect(self.checkbox_state_changed)
                    linePrecio = QLineEdit()
                    self.ui.tableDetalleFactura.setItem(index, 0, id_extintor)
                    self.ui.tableDetalleFactura.setCellWidget(index, 1, checkbox)
                    self.ui.tableDetalleFactura.setCellWidget(index, 2, linePrecio)
                    linePrecio.textChanged.connect(self.actualizar_precio_fila)
                    if extintor.id in self.selected_extintores:
                        checkbox.setChecked(True)
                        
                self.ui.tableDetalleFactura.setColumnWidth(1, 80)
    
    def checkbox_state_changed(self, state):
        checkbox = self.sender()
        extintor_id = checkbox.property("extintor_id")
        for fila in range(self.ui.tableDetalleFactura.rowCount()):
            item = self.ui.tableDetalleFactura.item(fila, 0)
            if item and item.data(QtCore.Qt.ItemDataRole.UserRole) == extintor_id:
                line_edit = self.ui.tableDetalleFactura.cellWidget(fila, 2)
                if state == Qt.CheckState.Checked.value:
                    precio = Extintor.recharge_prices(extintor_id=extintor_id)
                    self.selected_extintores[extintor_id] = precio.valor_num
                    line_edit.textChanged.emit(line_edit.text())
                else:
                    if extintor_id in self.selected_extintores:
                        del self.selected_extintores[extintor_id]
                        line_edit.textChanged.emit(line_edit.text())
                break

    def actualizar_precio_fila(self, texto):
        line_edit = self.sender()
        for fila in range(self.ui.tableDetalleFactura.rowCount()):
            if self.ui.tableDetalleFactura.cellWidget(fila, 2) == line_edit:
                extintor_id = self.ui.tableDetalleFactura.item(fila, 0).data(QtCore.Qt.ItemDataRole.UserRole)
                if texto:
                    try:
                        precio_extra = float(texto)
                        if extintor_id in self.selected_extintores:
                            precio_base = self.selected_extintores[extintor_id]
                            precio_total = precio_base + precio_extra
                        else:
                            precio_total = precio_extra
                        self.ui.tableDetalleFactura.setItem(fila, 3, QTableWidgetItem(str(precio_total)))
                    except ValueError:
                        pass
                else:
                    if extintor_id in self.selected_extintores:
                        self.ui.tableDetalleFactura.setItem(fila, 3, QTableWidgetItem(str(self.selected_extintores[extintor_id])))
                    else:
                        self.ui.tableDetalleFactura.setItem(fila, 3, QTableWidgetItem(""))
                break
        self.calcular_total()        
    
    def calcular_total(self): #Temporal, agregar mas campos/tareas?
        total = 0
        for fila in range(self.ui.tableDetalleFactura.rowCount()):
            item = self.ui.tableDetalleFactura.item(fila, 3)
            if item and item.text():
                try:
                    valor = float(item.text())
                    total += valor
                except ValueError:
                    pass
        self.ui.labelTotalAmount.setText(f"{total:.2f}")