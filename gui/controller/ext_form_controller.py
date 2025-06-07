from gui.controller import *
from models import *
from utils import get_image
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QIntValidator
from PyQt6 import QtCore

class ExtFormController(QDialog):
    def __init__(self,ui,extintor_controller, extintor_id=None, agregar_extintor_controller=None, precios_controller=None):
        super().__init__()
        self.ui = ui
        self.extintor_controller = extintor_controller
        self.agregar_extintor_controller=agregar_extintor_controller
        self.extintor_id = extintor_id
        self.precios_controller=precios_controller
        if self.extintor_id:
            self.cargar_datos_extintor()
        self.ui.guardar_extintor.clicked.connect(self.guardar_extintor)
        self.ui.cancelar_form.clicked.connect(self.cerrar_form)
        self.ui.setWindowTitle("Registrar Extintor")
        self.llenar_combobox()
        self.ui.label.setPixmap(QPixmap(get_image("extintor")))
        self.ui.lineEdit_numeracion.setValidator(QIntValidator(1,9999)) #Cambiar este validador debido a que tiene que aceptar mas numeris
    
    def cerrar_form(self):
        self.ui.close()
        self.ui.lineEdit_numeracion.clear()
        self.ui.comboBox_marca.clear()
        self.ui.lineEdit_ubicacion.clear()
        self.ui.comboBox_tipo.clear()
        self.ui.comboBox_capacidad.clear()
        self.extintor_id = None
    
    def limpiar_formulario(self):
        self.ui.lineEdit_numeracion.clear()
        self.ui.comboBox_marca.clear()
        self.ui.lineEdit_ubicacion.clear()
        self.ui.comboBox_tipo.clear()
        self.ui.comboBox_capacidad.clear()
    
    def cargar_datos_extintor(self):
        extintor = Extintor.get_by_id(self.extintor_id)
        if extintor:
            self.ui.lineEdit_numeracion.setText(str(extintor.numeracion))
            self.ui.comboBox_marca.currentData(QtCore.Qt.ItemDataRole.UserRole)
            self.ui.lineEdit_ubicacion.setText(extintor.ubicacion)
            self.ui.comboBox_tipo.currentData(QtCore.Qt.ItemDataRole.UserRole)
            self.ui.comboBox_capacidad.currentData(QtCore.Qt.ItemDataRole.UserRole)

    def obtener_datos(self):
        numeracion = self.ui.lineEdit_numeracion.text()
        marca = self.ui.comboBox_marca.currentData(QtCore.Qt.ItemDataRole.UserRole)
        ubicacion = self.ui.lineEdit_ubicacion.text()
        tipo = self.ui.comboBox_tipo.currentData(QtCore.Qt.ItemDataRole.UserRole)
        capacidad = self.ui.comboBox_capacidad.currentData(QtCore.Qt.ItemDataRole.UserRole)

        return(numeracion,marca,ubicacion,tipo,capacidad)
    
    def guardar_extintor(self):
        numeracion, marca, ubicacion, tipo, capacidad = self.obtener_datos()
        if not numeracion or not marca or not ubicacion or not tipo or not capacidad:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Por favor, completa todos los campos.")
            msg.exec()
            return
        if self.extintor_id:
            if Extintor.actualizar(self.extintor_id, numeracion, marca, ubicacion, tipo, capacidad):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Éxito")
                msg.setText("Extintor actualizado correctamente.")
                msg.exec()
        else:
            if Extintor.registrar(numeracion, marca, ubicacion, tipo, capacidad):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Éxito")
                msg.setText("Extintor registrado correctamente.")
                msg.exec()
        self.extintor_controller.mostrar_extintores()
        if self.agregar_extintor_controller:
            self.agregar_extintor_controller.cargar_datos()
        if self.precios_controller:
            self.precios_controller.cargar_precio_nuevos()
            self.precios_controller.cargar_precio_recargas()
        self.ui.close()
        self.limpiar_formulario()
        self.llenar_combobox()

    def llenar_combobox(self):
        self.ui.comboBox_marca.clear()
        self.ui.comboBox_tipo.clear()
        self.ui.comboBox_capacidad.clear()
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