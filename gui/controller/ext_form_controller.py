from gui.controller import *
from models import *
from PyQt6.QtWidgets import QDialog, QMessageBox

class ExtFormController(QDialog):
    def __init__(self,ui,extintor_controller, extintor_id=None):
        super().__init__()
        self.ui = ui
        self.extintor_controller = extintor_controller
        self.extintor_id = extintor_id
        if self.extintor_id: 
            self.cargar_datos_extintor()
        self.ui.guardar_extintor.clicked.connect(self.guardar_extintor)
        self.ui.cancelar_form.clicked.connect(self.cerrar_form)
        self.ui.setWindowTitle("Registrar Extintor")
        self.ui.comboBox_marca.addItems(["Marca 1", "Marca 2", "Marca 3"])
        self.ui.comboBox_tipo.addItems(["Tipo1", "Tipo2", "Tipo3"]) 
        self.ui.comboBox_capacidad.addItems(["5kg", "10kg", "20kg"])  
    
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
            self.ui.comboBox_marca.setCurrentText(extintor.marca)
            self.ui.lineEdit_ubicacion.setText(extintor.ubicacion)
            self.ui.comboBox_tipo.setCurrentText(extintor.tipo)
            self.ui.comboBox_capacidad.setCurrentText(extintor.capacidad)

    def obtener_datos(self):
        numeracion = self.ui.lineEdit_numeracion.text()
        marca = self.ui.comboBox_marca.currentText()
        ubicacion = self.ui.lineEdit_ubicacion.text()
        tipo = self.ui.comboBox_tipo.currentText()
        capacidad = self.ui.comboBox_capacidad.currentText()

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
        self.ui.close()
        self.limpiar_formulario()