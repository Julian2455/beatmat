from gui.controller import *
from models import *
from PyQt6.QtWidgets import QDialog, QMessageBox

class ClientFormController(QDialog):
    def __init__(self,ui,client_controller):
        super().__init__()
        self.ui = ui
        self.client_controller = client_controller
        self.ui.guardar_client.clicked.connect(self.registrar_cliente)
        self.ui.cancelar_form.clicked.connect(self.cerrar_form)
        self.ui.setWindowTitle("Registrar Cliente")
    
    def cerrar_form(self):
        self.ui.close()
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()

    def obtener_datos(self):
        nombre = self.ui.lineEdit.text().strip().title()
        direccion = self.ui.lineEdit_2.text().strip().title()
        return(nombre, direccion)
    
    def registrar_cliente(self):
        nombre, direccion = self.obtener_datos()
        
        if not nombre or not direccion:
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Por favor, completa todos los campos.")
            msg.exec()
            return
        if Cliente.registrar(nombre,direccion) == True:
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Exito")
            msg.setText("Cliente registrado correctamente.")
            msg.exec()
        self.client_controller.mostrar_clientes()
        self.ui.close() 
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()