from PyQt6.QtWidgets import QTableWidgetItem, QCheckBox, QDialog, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap, QDesktopServices
from PyQt6.QtCore import Qt, QUrl
from PyQt6 import QtWidgets
from models import *  
from utils import get_image
from utils import CardPDFGenerator 
import os

class ImpresionController(QDialog):
    def __init__(self,ui):
        super().__init__()
        self.ui = ui
        self.query=None
        self.marca_filter = None
        self.tipo_filter = None
        self.capacidad_filter = None
        self.checkboxes_impresion = []
        self.extintores_seleccionados = {} 
        self.pdf_generator = CardPDFGenerator()
        self.mostrar_extintores()
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.ui.imprimir.setIcon(QIcon(get_image("print")))
        self.ui.label.setPixmap(QPixmap(get_image("print")))
        self.ui.pushButton.setIcon(QIcon(get_image("buscar")))
        self.ui.pushButton_6.clicked.connect(self.restaurar_seleccionados)
        self.ui.cancelar_form.clicked.connect(self.cerrar_form)
        self.ui.lineEdit.textChanged.connect(self.buscar_extintor)
        self.ui.imprimir.clicked.connect(self.imprimir_tarjetas)

    def mostrar_extintores(self):
        if self.query or self.marca_filter or self.tipo_filter or self.capacidad_filter:
            extintores = Extintor.buscar_card(numeracion=self.query, marca_filter=self.marca_filter, 
                tipo_filter=self.tipo_filter, capacidad_filter=self.capacidad_filter)
        else:
            extintores = Extintor.show_all_card()
        self.ui.tableWidget.setRowCount(len(extintores))
        self.checkboxes_impresion = []
        for index, extintor in enumerate(extintores):
            id_extintor = QTableWidgetItem(str(extintor.numeracion))
            id_extintor.setData(Qt.ItemDataRole.UserRole, extintor.id)
            self.ui.tableWidget.setItem(index, 1, id_extintor)
            self.ui.tableWidget.setItem(index, 2, QTableWidgetItem(extintor.marca_nombre))
            self.ui.tableWidget.setItem(index, 3, QTableWidgetItem(extintor.tipo_nombre))
            self.ui.tableWidget.setItem(index, 4, QTableWidgetItem(extintor.capacidad_nombre))
            check = QCheckBox()
            id_ext = extintor.id
            seleccionado = self.extintores_seleccionados.get(id_ext, False)
            check.setChecked(seleccionado)
            if extintor.impreso:
                check.setEnabled(False)
            else:
                check.setEnabled(True)
            self.ui.tableWidget.setCellWidget(index, 0, check)
            check.stateChanged.connect(lambda state, cb=check, eid=id_ext: self.actualizar_seleccion(cb, eid))
            self.checkboxes_impresion.append(check)
            self.ui.tableWidget.resizeColumnToContents(0)
        
    def contador_select(self):
        total = len([eid for eid, marcado in self.extintores_seleccionados.items() if marcado])
        self.ui.contador.setText(f"Total seleccionado: {total}")
        if total >= 6:
            self.ui.contador.setText(f"Total seleccionado: {total} (límite)")
            self.ui.contador.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.ui.contador.setStyleSheet("color: black;")

    def mostrar_btn_restaurar(self):
        hay_seleccion = any(self.extintores_seleccionados.values())
        self.ui.pushButton_6.setVisible(hay_seleccion)
    
    def restaurar_seleccionados(self):
        self.extintores_seleccionados.clear()
        for cb in self.checkboxes_impresion:
            cb.blockSignals(True)
            cb.setChecked(False)
            cb.setEnabled(True)
            cb.blockSignals(False)
        self.contador_select()
        self.mostrar_extintores()
        self.ui.pushButton_6.setVisible(False)

    def actualizar_seleccion(self, checkbox, extintor_id):
        self.extintores_seleccionados[extintor_id] = checkbox.isChecked()
        self.limitar_seleccion_checkboxes(checkbox)
        self.contador_select()
        self.mostrar_btn_restaurar()

    def limitar_seleccion_checkboxes(self, checkbox):
        seleccionados = [eid for eid, marcado in self.extintores_seleccionados.items() if marcado]
        cantidad_seleccionados = len(seleccionados)
        if cantidad_seleccionados > 6:
            checkbox.blockSignals(True)
            checkbox.setChecked(False)
            checkbox.blockSignals(False)
            return
        if cantidad_seleccionados == 6:
            for cb in self.checkboxes_impresion:
                if not cb.isChecked():
                    cb.setEnabled(False)
        else:
            for cb in self.checkboxes_impresion:
                if not cb.isEnabled() and not cb.isChecked():
                    cb.setEnabled(True)

    def cerrar_form(self):
        self.restaurar_seleccionados()
        self.ui.close()
    
    def buscar_extintor(self):
        self.query = self.ui.lineEdit.text()
        self.mostrar_extintores()
    
    def imprimir_tarjetas(self):
        extintores_seleccionados_ids = [eid for eid, marcado in self.extintores_seleccionados.items() if marcado]
        if not extintores_seleccionados_ids:
            QMessageBox.warning(self.ui, "Advertencia", "No hay extintores seleccionados para imprimir.")
            return
        try:
            extintores_data = self.obtener_datos_extintores(extintores_seleccionados_ids)
            pdf_path = self.pdf_generator.generar_pdf_tarjetas(extintores_data)
            self.marcar_como_impresos(extintores_seleccionados_ids)
            QMessageBox.information(
                self.ui, 
                "Éxito", 
                f"Tarjetas generadas exitosamente.\nArchivo: {os.path.basename(pdf_path)}"
            )
            QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.abspath(pdf_path)))
            self.restaurar_seleccionados()
        except Exception as e:
            QMessageBox.critical(self.ui, "Error", f"Error al generar las tarjetas: {str(e)}")
    
    def obtener_datos_extintores(self, extintores_ids):
        extintores_data = []
        for extintor_id in extintores_ids:
            extintor = Extintor.obtener_datos_para_tarjeta(extintor_id)
            if extintor:
                extintores_data.append(extintor)
        return extintores_data
    
    def marcar_como_impresos(self, extintores_ids):
        Extintor.marcar_como_impresos(extintores_ids)
        self.mostrar_extintores()