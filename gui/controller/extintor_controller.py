from PyQt6.QtWidgets import QTableWidgetItem, QMenu, QCheckBox, QMessageBox, QPushButton
from PyQt6.QtGui import QAction, QColor, QBrush, QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from models import *  
from utils import get_image

class ExtintorController:
    def __init__(self, ui):
        self.ui = ui
        self.query=None
        self.marca_filter = None
        self.tipo_filter = None
        self.capacidad_filter = None
        self.pagina_actual = 1 
        self.filas_por_pagina = 10  
        self.total_extintores = Extintor.contar_extintores()
        self.total_paginas = (self.total_extintores // self.filas_por_pagina) + (1 if self.total_extintores % self.filas_por_pagina else 0)
        self.mostrar_extintores()
        self.llenar_combobox_filtro()
        self.ui.pushButton_2.clicked.connect(self.pagina_anterior) 
        self.ui.pushButton.clicked.connect(self.pagina_siguiente) 
        self.ui.pushButton_3.clicked.connect(self.primer_pagina) 
        self.ui.pushButton_4.clicked.connect(self.ultima_pagina) 
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.doubleClicked.connect(self.mostrar_detalles_extintor)
        self.ui.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.tableWidget.customContextMenuRequested.connect(self.mostrar_menu_contextual)
        self.edit_form_ext = None
        self.ui.lineEdit.textChanged.connect(self.buscar_extintor)
        self.ui.label.setPixmap(QPixmap(get_image("buscar")))
        self.ui.pushButton.setIcon(QIcon(get_image("sssiguiente"))) 
        self.ui.pushButton_2.setIcon(QIcon(get_image("anterior"))) 
        self.ui.pushButton_3.setIcon(QIcon(get_image("anterior_1"))) 
        self.ui.pushButton_4.setIcon(QIcon(get_image("proximo_1"))) 
        self.ui.pushButton_5.setIcon(QIcon(get_image("extintor")))
        self.ui.comboBox_marca.currentIndexChanged.connect(self.filtrar_por_marca)
        self.ui.comboBox_tipo.currentIndexChanged.connect(self.filtrar_por_tipo)
        self.ui.comboBox_capacidad.currentIndexChanged.connect(self.filtrar_por_capacidad)
        self.ui.btnRestaurarFiltros.clicked.connect(self.restaurar_filtros)

    def mostrar_extintores(self):
        if self.query or self.marca_filter or self.tipo_filter or self.capacidad_filter:
            extintores = Extintor.buscar(numeracion=self.query, marca_filter=self.marca_filter, 
                tipo_filter=self.tipo_filter, capacidad_filter=self.capacidad_filter,
                page=self.pagina_actual, per_page=self.filas_por_pagina)
        else:
            extintores = Extintor.show_all(page=self.pagina_actual, per_page=self.filas_por_pagina)
        self.ui.tableWidget.setRowCount(len(extintores))
        self.checkboxes_impresion = []
        for index, extintor in enumerate(extintores):
            id_extintor = QTableWidgetItem(str(extintor.numeracion))
            id_extintor.setData(Qt.ItemDataRole.UserRole, extintor.id)
            self.ui.tableWidget.setItem(index, 0, id_extintor)
            self.ui.tableWidget.setItem(index, 1, QTableWidgetItem(extintor.marca_nombre))
            self.ui.tableWidget.setItem(index, 2, QTableWidgetItem(extintor.ubicacion))
            self.ui.tableWidget.setItem(index, 3, QTableWidgetItem(extintor.tipo_nombre))
            self.ui.tableWidget.setItem(index, 4, QTableWidgetItem(extintor.capacidad_nombre))

        self.actualizar_estado_paginado()
        self.mostrar_boton_restaurar()
    
    def obtener_id_extintor(self):
        item_seleccionado = self.ui.tableWidget.currentItem()
        if item_seleccionado:
            fila = item_seleccionado.row()
            item_con_id = self.ui.tableWidget.item(fila, 0) 
            id_extintor = item_con_id.data(Qt.ItemDataRole.UserRole)
            return id_extintor
        return None
    
    def actualizar_estado_paginado(self):
        if self.query or self.marca_filter or self.tipo_filter or self.capacidad_filter:
            self.total_extintores = Extintor.contar_buscar(
                numeracion=self.query, marca_filter=self.marca_filter, tipo_filter=self.tipo_filter, 
                capacidad_filter=self.capacidad_filter)
        else:
            self.total_extintores = Extintor.contar_extintores()
        self.total_paginas = (self.total_extintores // self.filas_por_pagina) + (1 if self.total_extintores % self.filas_por_pagina else 0)
        self.ui.label_7.setText(f"Página {self.pagina_actual} de {self.total_paginas}")
        self.ui.label_7.repaint()
        self.ui.pushButton_2.setEnabled(self.pagina_actual > 1)
        self.ui.pushButton.setEnabled(self.pagina_actual < self.total_paginas)

    def pagina_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.mostrar_extintores()

    def pagina_siguiente(self):
        self.total_extintores = Extintor.contar_extintores()
        self.total_paginas = (self.total_extintores // self.filas_por_pagina) + (1 if self.total_extintores % self.filas_por_pagina else 0)

        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.mostrar_extintores()
    
    def primer_pagina(self):
        if self.pagina_actual != 1:
            self.pagina_actual = 1
            self.mostrar_extintores()

    def ultima_pagina(self):
        if self.pagina_actual != self.total_paginas:
            self.pagina_actual = self.total_paginas
            self.mostrar_extintores()
    
    def mostrar_detalles_extintor(self, index):
        numeracion = self.ui.tableWidget.item(index.row(), 0).text()
        self.details_ui.labelExtintores.setText(f"Detalles del Extintor {numeracion}")
        id_extintor=self.obtener_id_extintor()
        self.details_ui.extintor_id_actual = id_extintor
        self.ui.hide()
        self.details_ui.show()
        self.details_ui.btnAtras.setIcon(QIcon(get_image("btn-atras")))
        self.details_ui.tableWidgetExtintores.verticalHeader().setVisible(False)
        self.details_ui.tableWidgetTareas.horizontalHeader().setVisible(False)
        self.details_ui.tableWidgetExtintores.setRowCount(0)
        self.details_ui.tableWidgetTareas.setColumnCount(0)
        recargas=Recarga.show_filter(id_extintor)
        if recargas:
            self.details_ui.tableWidgetExtintores.setRowCount(len(recargas))
            for index, recarga in enumerate(recargas):
                id_recarga = QTableWidgetItem(str(recarga.vto_control_recarga_formateado))
                id_recarga.setData(Qt.ItemDataRole.UserRole, recarga.id)
                self.details_ui.tableWidgetExtintores.setItem(index, 0, id_recarga)
                self.details_ui.tableWidgetExtintores.setItem(index, 1, QTableWidgetItem(str(recarga.nuevo_control_recarga_formateado)))
                self.details_ui.tableWidgetExtintores.setItem(index, 2, QTableWidgetItem(str(recarga.vto_ph)))
                self.details_ui.tableWidgetExtintores.setItem(index, 3, QTableWidgetItem(str(recarga.fecha_fabricacion)))
        tareas=Tareas.show_filter(id_extintor)
        if tareas:
            num_tareas = len(tareas)
            self.details_ui.tableWidgetTareas.setColumnCount(num_tareas)
            self.observaciones={}
            for col, tarea in enumerate(tareas):
                id_item = QTableWidgetItem("")
                id_item.setData(Qt.ItemDataRole.UserRole, tarea.id)
                self.details_ui.tableWidgetTareas.setItem(0, col, id_item)
                self.observaciones[col] = tarea.observacion
                valores = [
                    tarea.fecha_formateada,
                    tarea.tamizacion,
                    tarea.peso,      
                    tarea.control_tacho,
                    tarea.relleno_polvo,
                    tarea.cambio_manometro,
                    tarea.oring,
                    tarea.gatillo,
                    tarea.pintura,
                    tarea.interior,
                    tarea.valvula,
                    tarea.bastago_bronce,
                    tarea.otro,
                ]
                for fila, valor in enumerate(valores):
                    item = QTableWidgetItem("")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    if fila < 13 and fila!=0:
                        if valor==True:
                            item.setText("SI")
                            item.setForeground(QBrush(QColor("green")))
                        else:
                            item.setText("NO")
                            item.setForeground(QBrush(QColor("red")))
                    else:
                        item.setText(str(valor))
                        if fila == 0:
                            font = QFont()
                            font.setBold(True)
                            item.setFont(font)
                    self.details_ui.tableWidgetTareas.setItem(fila, col, item)
                if tarea.observacion and tarea.observacion != "Null":
                    btn = QPushButton("Ver")
                    btn.clicked.connect(lambda checked, c=col: self.mostrar_observacion(c))
                    self.details_ui.tableWidgetTareas.setCellWidget(13, col, btn)
                self.details_ui.tableWidgetTareas.setColumnWidth(col,85)
    
    def mostrar_observacion(self, columna):
        observacion = self.observaciones.get(columna, "No hay observación")  
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Observación")
        msg.setText(observacion)
        msg.exec()

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
        editar_action.triggered.connect(self.editar_extintor)
        eliminar_action.triggered.connect(self.eliminar_extintor)
        menu.addAction(editar_action)
        menu.addAction(eliminar_action)
        menu.exec(self.ui.tableWidget.viewport().mapToGlobal(pos))
    
    def set_edit_form_ext(self, edit_form_ext):
        self.edit_form_ext = edit_form_ext

    def editar_extintor(self):
        id_extintor = self.obtener_id_extintor()
        if id_extintor and self.edit_form_ext:
            self.edit_form_ext.setWindowTitle("Editar Extintor")
            extintor = Extintor.get_by_id(id_extintor)
            if extintor:
                self.edit_form_ext.label_2.setText("EDITAR EXTINTOR")
                self.edit_form_ext.lineEdit_numeracion.setText(str(extintor.numeracion))
                self.edit_form_ext.comboBox_marca.clear()
                self.edit_form_ext.comboBox_tipo.clear()
                self.edit_form_ext.comboBox_capacidad.clear()
                marcas = Marca.show_all()
                marca_index_to_select = 0
                for i, marca in enumerate(marcas):
                    self.edit_form_ext.comboBox_marca.addItem(marca.nombre)
                    index = self.edit_form_ext.comboBox_marca.count() - 1
                    self.edit_form_ext.comboBox_marca.setItemData(index, marca.id, QtCore.Qt.ItemDataRole.UserRole)
                    if marca.id == extintor.marca_id:
                        marca_index_to_select = i
                tipos = Tipo.show_all()
                tipo_index_to_select = 0
                for i, tipo in enumerate(tipos):
                    self.edit_form_ext.comboBox_tipo.addItem(tipo.nombre)
                    index = self.edit_form_ext.comboBox_tipo.count() - 1
                    self.edit_form_ext.comboBox_tipo.setItemData(index, tipo.id, QtCore.Qt.ItemDataRole.UserRole)
                    if tipo.id == extintor.tipo_id:
                        tipo_index_to_select = i
                capacidades = Capacidad.show_all()
                capacidad_index_to_select = 0
                for i, capacidad in enumerate(capacidades):
                    self.edit_form_ext.comboBox_capacidad.addItem(capacidad.nombre)
                    index = self.edit_form_ext.comboBox_capacidad.count() - 1
                    self.edit_form_ext.comboBox_capacidad.setItemData(index, capacidad.id, QtCore.Qt.ItemDataRole.UserRole)
                    if capacidad.id == extintor.capacidad_id:
                        capacidad_index_to_select = i
                self.edit_form_ext.comboBox_marca.setCurrentIndex(marca_index_to_select)
                self.edit_form_ext.comboBox_tipo.setCurrentIndex(tipo_index_to_select)
                self.edit_form_ext.comboBox_capacidad.setCurrentIndex(capacidad_index_to_select)
                self.edit_form_ext.lineEdit_ubicacion.setText(str(extintor.ubicacion))
                self.edit_extintor_controller.extintor_id = id_extintor
                self.edit_form_ext.mostrar_form()

    def eliminar_extintor(self):
        id_extintor = self.obtener_id_extintor()
        if id_extintor:
            print(f"Eliminar : {id_extintor}")
    
    def actualizar_tablas(self, id_extintor): #Esta es casi igual a mostrar_detalles_extintor, tuve que hacerla por que no podia llamar a ese metodo sin el index de la columna
        extintor = Extintor.get_by_id(id_extintor)
        self.details_ui.labelExtintores.setText(f"Detalles del Extintor {extintor.numeracion}")
        self.ui.hide()
        self.details_ui.show()
        self.details_ui.tableWidgetExtintores.verticalHeader().setVisible(False)
        self.details_ui.tableWidgetTareas.horizontalHeader().setVisible(False)
        self.details_ui.tableWidgetExtintores.setRowCount(0)
        self.details_ui.tableWidgetTareas.setColumnCount(0) 
        recargas=Recarga.show_filter(id_extintor)
        if recargas:
            self.details_ui.tableWidgetExtintores.setRowCount(len(recargas))
            for index, recarga in enumerate(recargas):
                id_recarga = QTableWidgetItem(str(recarga.vto_control_recarga_formateado))
                id_recarga.setData(Qt.ItemDataRole.UserRole, recarga.id)
                self.details_ui.tableWidgetExtintores.setItem(index, 0, id_recarga)
                self.details_ui.tableWidgetExtintores.setItem(index, 1, QTableWidgetItem(str(recarga.nuevo_control_recarga_formateado)))
                self.details_ui.tableWidgetExtintores.setItem(index, 2, QTableWidgetItem(str(recarga.vto_ph)))
                self.details_ui.tableWidgetExtintores.setItem(index, 3, QTableWidgetItem(str(recarga.fecha_fabricacion)))       
        tareas = Tareas.show_filter(id_extintor)
        if tareas:
            num_tareas = len(tareas)
            self.details_ui.tableWidgetTareas.setColumnCount(num_tareas)
            self.observaciones={}
            for col, tarea in enumerate(tareas):
                id_item = QTableWidgetItem("")
                id_item.setData(Qt.ItemDataRole.UserRole, tarea.id)
                self.details_ui.tableWidgetTareas.setItem(0, col, id_item)
                self.observaciones[col] = tarea.observacion
                valores = [
                    tarea.fecha_formateada,
                    tarea.tamizacion,
                    tarea.peso,      
                    tarea.control_tacho,
                    tarea.relleno_polvo,
                    tarea.cambio_manometro,
                    tarea.oring,
                    tarea.gatillo,
                    tarea.pintura,
                    tarea.interior,
                    tarea.valvula,
                    tarea.bastago_bronce,
                    tarea.otro,
                ]
                for fila, valor in enumerate(valores):
                    item = QTableWidgetItem("")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    if fila < 13 and fila!=0:
                        if valor==True:
                            item.setText("SI")
                            item.setForeground(QBrush(QColor("green")))
                        else:
                            item.setText("NO")
                            item.setForeground(QBrush(QColor("red")))
                    else:
                        item.setText(str(valor))
                        if fila == 0:
                            font = QFont()
                            font.setBold(True)
                            item.setFont(font)
                    self.details_ui.tableWidgetTareas.setItem(fila, col, item)
                if tarea.observacion and tarea.observacion != "Null":
                    btn = QPushButton("Ver")
                    btn.clicked.connect(lambda checked, c=col: self.mostrar_observacion(c))
                    self.details_ui.tableWidgetTareas.setCellWidget(13, col, btn)
                self.details_ui.tableWidgetTareas.setColumnWidth(col,85)
    
    def buscar_extintor(self):
        previous_query = self.query
        self.query = self.ui.lineEdit.text()
        if previous_query != self.query:
            self.pagina_actual = 1
        self.mostrar_extintores()
    
    def llenar_combobox_filtro(self):
        self.ui.comboBox_marca.clear()
        self.ui.comboBox_tipo.clear()
        self.ui.comboBox_capacidad.clear()
        self.ui.comboBox_marca.addItem("Marca")
        self.ui.comboBox_tipo.addItem("Tipo")
        self.ui.comboBox_capacidad.addItem("Capacidad")
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
        self.mostrar_extintores()

    def filtrar_por_tipo(self):
        indice = self.ui.comboBox_tipo.currentIndex()
        if indice == 0:
            self.tipo_filter = None
        else:
            self.tipo_filter = self.ui.comboBox_tipo.itemData(indice, QtCore.Qt.ItemDataRole.UserRole)
        self.pagina_actual = 1
        self.mostrar_extintores()

    def filtrar_por_capacidad(self):
        indice = self.ui.comboBox_capacidad.currentIndex()
        if indice == 0:
            self.capacidad_filter = None
        else:
            self.capacidad_filter = self.ui.comboBox_capacidad.itemData(indice, QtCore.Qt.ItemDataRole.UserRole)
        self.pagina_actual = 1
        self.mostrar_extintores()

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
        self.mostrar_extintores()
    