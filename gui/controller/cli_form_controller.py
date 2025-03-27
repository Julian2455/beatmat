from gui.controller import *
from models import *
from PyQt6.QtWidgets import QDialog, QMessageBox

class ClientFormController(QDialog):
    def __init__(self,ui,client_controller, main_window):
        super().__init__()
        self.ui = ui
        self.client_controller = client_controller
        self.main_window = main_window
        self.ui.guardar_client.clicked.connect(self.registrar_cliente)
        self.ui.cancelar_form.clicked.connect(self.cerrar_form)
        self.ui.setWindowTitle("Registrar Cliente")
        self.main_window.cambios_edit.clicked.connect(self.actualizar)
        self.main_window.cerrar_edit.clicked.connect(self.cerrar_form_edit)
    
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

    def abrir_form_edit(self,cliente):
        client_id , nombrec, direccionc = cliente
        self.main_window.lineEdit_3.setText(str(client_id))
        self.main_window.lineEdit_3.setDisabled(True)
        self.main_window.lineEdit.setText(nombrec)
        self.main_window.lineEdit_2.setText(direccionc)
        self.main_window.mostrar_form_edit()
    
    def actualizar(self):
        client_id = self.main_window.lineEdit_3.text()
        nombrec = self.main_window.lineEdit.text().title()
        direccionc = self.main_window.lineEdit_2.text().title()

        if not nombrec or not direccionc or not client_id:
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Por favor, completa todos los campos.")
            msg.exec()
            return
        if Cliente.actualizar(client_id,nombrec,direccionc) == True:
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Exito")
            msg.setText("Cliente editado correctamente.")
            msg.exec()
        self.client_controller.mostrar_clientes()
        self.main_window.close()

    def cerrar_form_edit(self):
        self.main_window.close()
        self.main_window.lineEdit.clear()
        self.main_window.lineEdit_2.clear()