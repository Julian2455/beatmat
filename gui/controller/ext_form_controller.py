from gui.controller import *
from models import *
from PyQt6.QtWidgets import QDialog, QMessageBox

class ExtFormController(QDialog):
    def __init__(self,ui,extintor_controller):
        super().__init__()
        self.ui = ui
        self.extintor_controller = extintor_controller
        self.ui.guardar_extintor.clicked.connect(self.registrar_extintor)
        self.ui.cancelar_form.clicked.connect(self.cerrar_form)
        self.ui.setWindowTitle("Registrar Extintor")
    
    def cerrar_form(self):
        self.ui.close()
        self.ui.lineEdit_numeracion.clear()
        self.ui.comboBox_marca.clear()
        self.ui.lineEdit_ubicacion.clear()
        self.ui.comboBox_tipo.clear()
        self.ui.comboBox_capacidad.clear()

    def obtener_datos(self):
        numeracion = self.ui.lineEdit_numeracion.text()
        marca = self.ui.comboBox_marca.currentText()
        ubicacion = self.ui.lineEdit_ubicacion.text()
        tipo = self.ui.comboBox_tipo.currentText()
        capacidad = self.ui.comboBox_capacidad.currentText()

        return(numeracion,marca,ubicacion,tipo,capacidad)
    
    def registrar_extintor(self):
        numeracion,marca,ubicacion,tipo,capacidad = self.obtener_datos()
        
        if not numeracion or not marca or not ubicacion or not tipo or not capacidad:
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Por favor, completa todos los campos.")
            msg.exec()
            return
        if Extintor.registrar(numeracion,marca,ubicacion,tipo,capacidad) == True:
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Exito")
            msg.setText("Extintor registrado correctamente.")
            msg.exec()
        self.extintor_controller.mostrar_extintores()
        self.ui.close() 
        self.ui.lineEdit_numeracion.clear()
        self.ui.comboBox_marca.clear()
        self.ui.lineEdit_ubicacion.clear()
        self.ui.comboBox_tipo.clear()
        self.ui.comboBox_capacidad.clear()