from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from models import *
from utils import get_image
from PyQt6.QtGui import QIcon, QDoubleValidator, QPixmap
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QObject, QLocale

class MtcController(QObject):
    def __init__(self,ui, extintor_controller, extintor_form_controller):
        super().__init__()
        self.ui = ui
        self.extintor_controller = extintor_controller
        self.extintor_form_controller = extintor_form_controller
        self.tipo_formulario = None
        self.ui.guardar_detalle.clicked.connect(self.guardar_detalle)
        self.ui.cancelar_form.clicked.connect(self.cancelar)
        self.ui.label.setPixmap(QPixmap(get_image("config2")))

    def cancelar(self):
        self.ui.close()
        self.ui.lineEdit.clear()
    
    def limpiar_formulario(self):
        self.ui.lineEdit.clear()

    def mostrar_form(self, tipo):
        self.tipo_formulario = tipo
        self.ui.label_config.setText(f"Registrar {tipo}")
        self.ui.nombre_detalle.setText(f"{tipo}")
        if tipo == "Marca":
            datos = Marca.show_all()
            self.ui.label_registro.setText(f"{tipo}s registradas")
        elif tipo == "Tipo":
            datos = Tipo.show_all()
            self.ui.label_registro.setText(f"{tipo}s registrados")
        elif tipo == "Capacidad":
            datos = Capacidad.show_all()
            self.ui.label_registro.setText(f"{tipo}es registradas")
        else:
            datos = []
        self.ui.tableWidget.setRowCount(len(datos))
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.horizontalHeader().setVisible(False)
        for index, dato in enumerate(datos):
            self.ui.tableWidget.setItem(index, 0, QTableWidgetItem(dato.nombre))
        self.ui.show()
        
    
    def guardar_detalle(self):
        tipo = self.tipo_formulario
        nombre = self.ui.lineEdit.text()
        if not nombre or not tipo:
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error")
            msg.setText(f"Por favor, completa el campo de {tipo}. Es obligatorio.")
            msg.exec()
            return
        if tipo == "Marca":
            if Marca.registrar_marca(nombre) == True:
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Exito")
                msg.setText(f"Marca '{nombre}' registrada correctamente.")
                msg.exec()
        elif tipo == "Tipo":
            if Tipo.registrar_tipo(nombre) == True:
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Exito")
                msg.setText(f"Tipo '{nombre}' registrado correctamente.")
                msg.exec()
        elif tipo == "Capacidad":
            if Capacidad.registrar_capacidad(nombre) == True:
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Exito")
                msg.setText(f"Capacidad '{nombre}' registrada correctamente.")
                msg.exec()
        self.extintor_controller.llenar_combobox_filtro()
        self.extintor_form_controller.llenar_combobox()
        self.ui.close()
        self.limpiar_formulario()