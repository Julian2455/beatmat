from PyQt6.QtWidgets import QTableWidgetItem, QPushButton, QMessageBox, QMenu, QHeaderView, QCheckBox, QHBoxLayout, QWidget
from PyQt6.QtGui import QAction, QColor, QPixmap, QIcon
from PyQt6.QtCore import Qt, QObject
from PyQt6 import QtWidgets, QtCore
from models import *  
from utils import get_image

class CajaFormController(QObject):
    def __init__(self, ui, caja_controller, cliente_id=None):
        super().__init__()
        self.ui = ui
        self.caja_controller = caja_controller
        self.cliente_id = cliente_id
        self.query=None
        self.marca_filter = None
        self.tipo_filter = None
        self.capacidad_filter = None
        self.selected_extintores={}
        self.pagina_actual = 1 
        self.filas_por_pagina = 10
        self.total_extintores = Extintor.contar_buscar(numeracion=self.query, marca_filter=self.marca_filter, tipo_filter=self.tipo_filter, capacidad_filter=self.capacidad_filter, disponible=True)
        self.total_paginas = (self.total_extintores // self.filas_por_pagina) + (1 if self.total_extintores % self.filas_por_pagina else 0)  
        self.ui.tableExtintores.verticalHeader().setVisible(False)
        self.ui.btnPreviousPage.clicked.connect(self.pagina_anterior) 
        self.ui.btnNextPage.clicked.connect(self.pagina_siguiente) 
        self.ui.btnFirstPage.clicked.connect(self.primer_pagina) 
        self.ui.btnLastPage.clicked.connect(self.ultima_pagina) 
        header = self.ui.tableExtintores.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.ui.tableExtintores.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.cargar_datos_usuario()
        self.cargar_datos()
        self.llenar_combobox_filtro()
        self.actualizar_estado_paginado()
        self.ui.labelTotal.setText("Seleccionados: 0")
        self.ui.lineFiltro.textChanged.connect(self.buscar_extintor)
        self.ui.comboBox_marca.currentIndexChanged.connect(self.filtrar_por_marca)
        self.ui.comboBox_tipo.currentIndexChanged.connect(self.filtrar_por_tipo)
        self.ui.comboBox_capacidad.currentIndexChanged.connect(self.filtrar_por_capacidad)
        self.ui.btnRestaurarFiltros.clicked.connect(self.restaurar_filtros)
        self.ui.btnAgregar.clicked.connect(self.add_selected)
        
    def cargar_datos_usuario(self):
        cliente=Cliente.get_by_id(self.cliente_id)
        self.ui.labelCliente.setText(f"Cliente: {cliente.nombre}")
    
    def cargar_datos(self):
        self.ui.tableExtintores.setRowCount(0)
        extintores = Extintor.buscar(numeracion=self.query, marca_filter=self.marca_filter, 
                tipo_filter=self.tipo_filter, capacidad_filter=self.capacidad_filter, 
                page=self.pagina_actual, per_page=self.filas_por_pagina,disponible=True)
        self.ui.tableExtintores.setRowCount(len(extintores))
        for index, extintor in enumerate(extintores):
            checkbox = QCheckBox()
            checkbox.setProperty("extintor_id", extintor.id)
            checkbox.setStyleSheet("QCheckBox { margin-left: 10px; }")
            checkbox.stateChanged.connect(self.checkbox_state_changed)
            if extintor.id in self.selected_extintores:
                checkbox.setChecked(True)
            self.ui.tableExtintores.setCellWidget(index, 0, checkbox)
            self.ui.tableExtintores.setItem(index, 1, QTableWidgetItem(str(extintor.numeracion)))
            self.ui.tableExtintores.setItem(index, 2, QTableWidgetItem(extintor.marca_nombre))
            self.ui.tableExtintores.setItem(index, 3, QTableWidgetItem(extintor.tipo_nombre))
            self.ui.tableExtintores.setItem(index, 4, QTableWidgetItem(extintor.capacidad_nombre))
        self.ui.tableExtintores.setColumnWidth(0, 40) 
        self.actualizar_estado_paginado()
        self.mostrar_boton_restaurar()
    
    def actualizar_estado_paginado(self):
        self.total_extintores = Extintor.contar_buscar(
            numeracion=self.query, marca_filter=self.marca_filter, tipo_filter=self.tipo_filter, 
            capacidad_filter=self.capacidad_filter, disponible=True)
        self.total_paginas = (self.total_extintores // self.filas_por_pagina) + (1 if self.total_extintores % self.filas_por_pagina else 0)
        self.ui.labelPageInfo.setText(f"Página {self.pagina_actual} de {self.total_paginas}")
        self.ui.labelPageInfo.repaint()
        self.ui.btnPreviousPage.setEnabled(self.pagina_actual > 1)
        self.ui.btnNextPage.setEnabled(self.pagina_actual < self.total_paginas)

    def pagina_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.cargar_datos()

    def pagina_siguiente(self):
        self.total_extintores = Extintor.contar_buscar(
            numeracion=self.query, marca_filter=self.marca_filter, 
            tipo_filter=self.tipo_filter, capacidad_filter=self.capacidad_filter, disponible=True)
        self.total_paginas = (self.total_extintores // self.filas_por_pagina) + (1 if self.total_extintores % self.filas_por_pagina else 0)
        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.cargar_datos()
    
    def primer_pagina(self):
        if self.pagina_actual != 1:
            self.pagina_actual = 1
            self.cargar_datos()

    def ultima_pagina(self):
        if self.pagina_actual != self.total_paginas:
            self.pagina_actual = self.total_paginas
            self.cargar_datos()
    
    def buscar_extintor(self):
        previous_query = self.query
        self.query = self.ui.lineFiltro.text()
        if previous_query != self.query:
            self.pagina_actual = 1
        self.cargar_datos()
    
    def llenar_combobox_filtro(self):
        self.ui.comboBox_marca.clear()
        self.ui.comboBox_tipo.clear()
        self.ui.comboBox_capacidad.clear()
        self.ui.comboBox_marca.addItem("----Marca----")
        self.ui.comboBox_tipo.addItem("----Tipo----")
        self.ui.comboBox_capacidad.addItem("----Capacidad----")
        marcas=Marca.show_all()
        for marca in marcas:
            self.ui.comboBox_marca.addItem(marca.nombre)
            index=self.ui.comboBox_marca.count()-1
            self.ui.comboBox_marca.setItemData(index, marca.id, QtCore.Qt.ItemDataRole.UserRole)
        tipos=Tipo.show_all()
        for tipo in tipos:
            self.ui.comboBox_tipo.addItem(tipo.nombre)
            index=self.ui.comboBox_tipo.count()-1
            self.ui.comboBox_tipo.setItemData(index, tipo.id, QtCore.Qt.ItemDataRole.UserRole)
        capacidades=Capacidad.show_all()
        for capacidad in capacidades:
            self.ui.comboBox_capacidad.addItem(capacidad.nombre)
            index=self.ui.comboBox_capacidad.count()-1
            self.ui.comboBox_capacidad.setItemData(index, capacidad.id, QtCore.Qt.ItemDataRole.UserRole)
    
    def filtrar_por_marca(self):
        indice = self.ui.comboBox_marca.currentIndex()
        if indice == 0:
            self.marca_filter = None
        else:
            self.marca_filter = self.ui.comboBox_marca.itemData(indice, QtCore.Qt.ItemDataRole.UserRole)
        self.pagina_actual = 1 
        self.cargar_datos()

    def filtrar_por_tipo(self):
        indice = self.ui.comboBox_tipo.currentIndex()
        if indice == 0:
            self.tipo_filter = None
        else:
            self.tipo_filter = self.ui.comboBox_tipo.itemData(indice, QtCore.Qt.ItemDataRole.UserRole)
        self.pagina_actual = 1
        self.cargar_datos()

    def filtrar_por_capacidad(self):
        indice = self.ui.comboBox_capacidad.currentIndex()
        if indice == 0:
            self.capacidad_filter = None
        else:
            self.capacidad_filter = self.ui.comboBox_capacidad.itemData(indice, QtCore.Qt.ItemDataRole.UserRole)
        self.pagina_actual = 1
        self.cargar_datos()

    def mostrar_boton_restaurar(self):
        filtros_activos = (
            self.ui.comboBox_marca.currentIndex() != 0 or
            self.ui.comboBox_tipo.currentIndex() != 0 or
            self.ui.comboBox_capacidad.currentIndex() != 0
        )
        self.ui.btnRestaurarFiltros.setVisible(filtros_activos)

    def restaurar_filtros(self):
        self.ui.comboBox_marca.setCurrentIndex(0)
        self.ui.comboBox_tipo.setCurrentIndex(0)
        self.ui.comboBox_capacidad.setCurrentIndex(0)
        self.marca_filter = None
        self.tipo_filter = None
        self.capacidad_filter = None
        self.pagina_actual = 1
        self.cargar_datos()
    
    def checkbox_state_changed(self, state):
        checkbox = self.sender()
        if not checkbox:
            print("---->>>>>> 1")
            return
        extintor_id = checkbox.property("extintor_id")
        if extintor_id is None:
            print("---->>>>>> 2")
            return
        if state == Qt.CheckState.Checked.value:
            self.selected_extintores[extintor_id] = True
        else:
            if extintor_id in self.selected_extintores:
                del self.selected_extintores[extintor_id]
                
        self.ui.labelTotal.setText(f"Seleccionados: {len(self.selected_extintores)}")
    
    def add_selected(self):
        extintores=list(self.selected_extintores.keys())
        if Extintor.asignar_cliente(extintores,self.cliente_id) == True:
            self.caja_controller.seleccionar_cliente()
            self.selected_extintores={}
            self.pagina_actual=1
            self.cargar_datos()
            self.ui.close()

    def reiniciar(self, cliente_id=None):
        if cliente_id:
            self.cliente_id = cliente_id
        self.query = None
        self.marca_filter = None
        self.tipo_filter = None
        self.capacidad_filter = None
        self.selected_extintores = {}
        self.pagina_actual = 1
        self.filas_por_pagina = 10
        self.total_extintores = Extintor.contar_buscar(numeracion=self.query, marca_filter=self.marca_filter, 
            tipo_filter=self.tipo_filter, capacidad_filter=self.capacidad_filter, disponible=True)
        self.total_paginas = (self.total_extintores // self.filas_por_pagina) + (1 if self.total_extintores % self.filas_por_pagina else 0)
        self.ui.labelTotal.setText("Seleccionados: 0")
        self.ui.lineFiltro.clear()
        self.ui.comboBox_marca.setCurrentIndex(0)
        self.ui.comboBox_tipo.setCurrentIndex(0)
        self.ui.comboBox_capacidad.setCurrentIndex(0)
        self.cargar_datos_usuario()
        self.cargar_datos()
        self.actualizar_estado_paginado()