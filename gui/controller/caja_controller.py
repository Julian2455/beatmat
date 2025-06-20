from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QMenu, QMessageBox, QCheckBox, QLineEdit
from models import *
from utils import get_image
from PyQt6.QtGui import QIcon, QAction, QDoubleValidator
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QDate, Qt, QObject, QLocale

class CajaController(QObject):
    def __init__(self,ui,historial_controller=None,print_controller=None, reportes_controller=None):
        super().__init__()
        self.ui = ui
        self.cliente=None
        self.historial_controller=historial_controller
        self.print_controller=print_controller
        self.reportes_controller=reportes_controller
        self.clientes_combobox()
        self.pagos_combobox()
        self.configurar_validadores()
        self.ui.comboClientes.currentIndexChanged.connect(self.seleccionar_cliente)
        self.ui.tableExtintoresCliente.verticalHeader().setVisible(False)
        self.ui.tableExtintoresCliente.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.ui.tableExtintoresCliente.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.comboClientes.editTextChanged.connect(self.seleccionar_cliente)
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.ui.btnAgregarExtintores.setVisible(False)
        self.ui.tableExtintoresCliente.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.tableExtintoresCliente.customContextMenuRequested.connect(self.mostrar_menu_contextual)
        self.selected_extintores={}
        self.selected_nuevos={}
        self.ui.lineCobro.setDisabled(True)
        self.ui.btnGuardar.clicked.connect(self.confirmar_compra) 
        self.ui.btnCancelar.clicked.connect(self.cancelar) 
        self.ui.lineCobro.textChanged.connect(self.cobrar)
    
    def clientes_combobox(self):
        self.ui.comboClientes.clear()
        self.ui.comboClientes.addItem("--SELECCIONAR CLIENTE--")
        clientes=Cliente.all()
        for cliente in clientes:
            self.ui.comboClientes.addItem(cliente.nombre)
            index=self.ui.comboClientes.count()-1
            self.ui.comboClientes.setItemData(index, cliente.id, QtCore.Qt.ItemDataRole.UserRole)
    
    def pagos_combobox(self):
        self.ui.comboMedioPago.clear()
        self.ui.comboMedioPago.addItem("--SELECCIONAR MEDIO DE PAGO--")
        metodos=CatPagos.show_all()
        for metodo in metodos:
            self.ui.comboMedioPago.addItem(metodo.nombre)
            index=self.ui.comboMedioPago.count()-1
            self.ui.comboMedioPago.setItemData(index, metodo.id, QtCore.Qt.ItemDataRole.UserRole)

    def configurar_validadores(self):
        self.validator = QDoubleValidator()
        self.validator.setDecimals(2)
        self.validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.locale = QLocale(QLocale.Language.Spanish)
        self.locale.setNumberOptions(QLocale.NumberOption.OmitGroupSeparator)
        self.validator.setLocale(self.locale)
        self.ui.lineCobro.setValidator(self.validator)

    def seleccionar_cliente(self):
        indice = self.ui.comboClientes.currentIndex()
        texto = self.ui.comboClientes.currentText()
        self.ui.tableExtintoresCliente.setRowCount(0)
        self.selected_extintores={}
        self.selected_nuevos={}
        if indice == 0 or texto=="":
            self.limpiar_campos()
        else:
            self.ui.lineCobro.setDisabled(False)
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
                for index, extintor in enumerate(extintores):
                    checkbox = QCheckBox()
                    checkbox.setProperty("extintor_id", extintor.id)
                    checkbox.setStyleSheet("QCheckBox { margin-left: 30px; }")
                    checkbox.setProperty("nuevo", False)
                    checkbox.stateChanged.connect(self.checkbox_state_changed)
                    linePrecio = QLineEdit()
                    linePrecio.setValidator(self.validator)
                    if extintor.nuevo==True:
                        checkboxn = QCheckBox()
                        checkboxn.setProperty("extintor_id", extintor.id)
                        checkboxn.setProperty("nuevo", True)
                        checkboxn.setStyleSheet("QCheckBox { margin-left: 30px; }")
                        checkboxn.stateChanged.connect(self.checkbox_state_changed)
                        checkboxn.setChecked(True)
                        self.ui.tableExtintoresCliente.setCellWidget(index, 5, checkboxn)
                        precio_nuevo = Extintor.new_prices(extintor_id=extintor.id)
                        if precio_nuevo:
                            self.selected_nuevos[extintor.id] = precio_nuevo.valor_num
                    self.ui.tableExtintoresCliente.setCellWidget(index, 6, checkbox)
                    self.ui.tableExtintoresCliente.setCellWidget(index, 7, linePrecio)
                    linePrecio.textChanged.connect(self.actualizar_precio_fila)
                self.actualizar_todos_precios()
    
    def checkbox_state_changed(self, state):
        checkbox = self.sender()
        extintor_id = checkbox.property("extintor_id")
        nuevo = checkbox.property("nuevo")
        if extintor_id is None:
            return
        for fila in range(self.ui.tableExtintoresCliente.rowCount()):
            item = self.ui.tableExtintoresCliente.item(fila, 0)
            if item and item.data(QtCore.Qt.ItemDataRole.UserRole) == extintor_id:
                line_edit = self.ui.tableExtintoresCliente.cellWidget(fila, 7)
                if line_edit is None:
                    continue
                if nuevo:
                    if state == Qt.CheckState.Checked.value:
                        precio = Extintor.new_prices(extintor_id=extintor_id)
                        if precio:
                            self.selected_nuevos[extintor_id] = precio.valor_num
                    else:
                        if extintor_id in self.selected_nuevos:
                            del self.selected_nuevos[extintor_id]
                else:
                    if state == Qt.CheckState.Checked.value:
                        precio = Extintor.recharge_prices(extintor_id=extintor_id)
                        if precio:
                            self.selected_extintores[extintor_id] = precio.valor_num
                    else:
                        if extintor_id in self.selected_extintores:
                            del self.selected_extintores[extintor_id]
                line_edit.textChanged.emit(line_edit.text())
                break
    
    def actualizar_todos_precios(self):
        for fila in range(self.ui.tableExtintoresCliente.rowCount()):
            line_edit = self.ui.tableExtintoresCliente.cellWidget(fila, 7)
            if line_edit:
                line_edit.textChanged.emit(line_edit.text())

    def actualizar_precio_fila(self, texto):
        line_edit = self.sender()
        for fila in range(self.ui.tableExtintoresCliente.rowCount()):
            if self.ui.tableExtintoresCliente.cellWidget(fila, 7) == line_edit:
                extintor_id = self.ui.tableExtintoresCliente.item(fila, 0).data(QtCore.Qt.ItemDataRole.UserRole)
                precio_total = 0
                if extintor_id in self.selected_extintores:
                    precio_total += self.selected_extintores[extintor_id]
                if extintor_id in self.selected_nuevos:
                    precio_total += self.selected_nuevos[extintor_id]
                if texto:
                    try:
                        precio_extra = self.locale.toDouble(texto)[0]
                        precio_total += precio_extra
                    except ValueError:
                        pass
                if precio_total > 0:
                    self.ui.tableExtintoresCliente.setItem(fila, 8, QTableWidgetItem(self.locale.toString(float(precio_total), 'f', 2)))
                else:
                    self.ui.tableExtintoresCliente.setItem(fila, 8, QTableWidgetItem(""))
                break
        self.calcular_total()    
    
    def calcular_total(self):
        total = 0
        for fila in range(self.ui.tableExtintoresCliente.rowCount()):
            item = self.ui.tableExtintoresCliente.item(fila, 8)
            if item and item.text():
                try:
                    valor = self.locale.toDouble(item.text())[0]
                    total += valor
                except ValueError:
                    pass
        self.ui.labelTotalAmount.setText(self.locale.toString(float(total), 'f', 2))
        self.ui.lineCobro.setText("")
        self.ui.lineAdeudado.setText("")
        self.total=total
    
    def cobrar(self):
        if hasattr(self, 'total') and self.total:
            texto = self.ui.lineCobro.text()
            if texto:
                try:
                    cobro = self.locale.toDouble(texto)[0]
                    deuda = self.total - cobro
                    self.ui.lineAdeudado.setText(self.locale.toString(float(deuda), 'f', 2))
                    if cobro<self.total:
                        self.ui.lineAdeudado.setStyleSheet("color:red;")
                    else:
                        self.ui.lineAdeudado.setStyleSheet("color:green;")
                except ValueError:
                    self.ui.lineAdeudado.setText("")
            else:
                self.ui.lineAdeudado.setText("")
        else:
            pass
    
    def confirmar_compra(self):
        medio_de_pago=self.ui.comboMedioPago.currentData(QtCore.Qt.ItemDataRole.UserRole)
        if not medio_de_pago:
            self.mostrar_error("Seleccione un medio de pago", "Debe seleccionar un medio de pago para continuar.")
            return
        if not self.cliente:
            self.mostrar_error("Seleccione un cliente", "Debe seleccionar un cliente para continuar.")
            return
        cobro = self.ui.lineCobro.text().strip()
        if not cobro:
            self.mostrar_error("Monto de cobro vacío", "Debe ingresar un monto de cobro.")
            return
        if not hasattr(self, 'total') or self.total <= 0:
            self.mostrar_error("Total inválido", "El total de la compra debe ser mayor a cero.")
            return
        precios_adicionales = {}
        precios_totales = {}
        cobro_num = self.locale.toDouble(cobro)[0]
        deuda = self.ui.lineAdeudado.text()
        if deuda:
            deuda_num = self.locale.toDouble(deuda)[0]
        else:
            deuda_num = 0
        fecha = self.ui.dateEdit.date().toPyDate()
        descripcion = self.ui.lineDescripcion.text()
        for fila in range(self.ui.tableExtintoresCliente.rowCount()):
            extintor_id = self.ui.tableExtintoresCliente.item(fila, 0).data(QtCore.Qt.ItemDataRole.UserRole)
            line_edit = self.ui.tableExtintoresCliente.cellWidget(fila, 7)
            if line_edit and line_edit.text():
                try:
                    precio_adicional = self.locale.toDouble(line_edit.text())[0]
                    if precio_adicional > 0:
                        precios_adicionales[extintor_id] = precio_adicional
                except ValueError:
                    pass
            item_total = self.ui.tableExtintoresCliente.item(fila, 8)
            if item_total and item_total.text():
                try:
                    precio_total = self.locale.toDouble(item_total.text())[0]
                    precios_totales[extintor_id] = precio_total
                except ValueError:
                    pass
        if not self.selected_extintores and not self.selected_nuevos and not precios_adicionales:
            self.mostrar_error("Sin valores seleccionados", "Debe asignar al menos un valor (nuevo, recarga u otros ).")
            return
        exito = Caja.confirmar_compra(
            self.cliente, fecha, self.total, cobro_num, deuda_num, 
            precios_totales, self.selected_extintores, self.selected_nuevos, 
            precios_adicionales,medio_de_pago, descripcion
        )
        if exito:
            self.mostrar_info("Compra registrada", "La compra se ha registrado correctamente.")
            self.limpiar_campos()
            if self.historial_controller:
                self.historial_controller.mostrar_ventas()
            if self.print_controller:
                self.print_controller.mostrar_extintores()
            if self.reportes_controller:
                self.reportes_controller.cargar_datos()
        else:
            self.mostrar_error("Error", "Ocurrió un error al registrar la compra.")

    def limpiar_campos(self):
        self.ui.lineCobro.setText("")
        self.ui.lineAdeudado.setText("")
        self.ui.lineDescripcion.setText("")
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.ui.labelTotalAmount.setText("0.00")
        self.ui.comboClientes.setCurrentIndex(0)
        self.ui.comboMedioPago.setCurrentIndex(0)
        self.ui.tableExtintoresCliente.setRowCount(0)
        self.selected_extintores = {}
        self.selected_nuevos = {}
        self.ui.lineCobro.setDisabled(True)
        self.cliente = None
        self.ui.btnAgregarExtintores.setVisible(False)
    
    def mostrar_error(self, titulo, mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
    
    def mostrar_info(self, titulo, mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
    
    def cancelar(self):
        self.limpiar_campos()