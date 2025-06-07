from gui.controller import *
from models import *
from utils import get_image
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QIntValidator

class ClientFormController(QDialog):
    def __init__(self,ui,client_controller,cliente_id=None,caja_controller=None):
        super().__init__()
        self.ui = ui
        self.client_controller = client_controller
        self.caja_controller = caja_controller
        self.cliente_id = cliente_id
        if self.cliente_id: 
            self.cargar_datos_cliente()
        self.ui.guardar_client.clicked.connect(self.guardar_cliente)
        self.ui.cancelar_form.clicked.connect(self.cerrar_form)
        self.ui.setWindowTitle("Registrar Cliente")
        self.ui.label.setPixmap(QPixmap(get_image("avatar")))
        self.ui.lineEdit_3.setValidator(QIntValidator(1,9999)) #Cambiar este validador debido a que tiene que aceptar mas numeris
    
    def cerrar_form(self):
        self.ui.close()
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
    
    def limpiar_formulario(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
    
    def cargar_datos_extintor(self):
        cliente = Cliente.get_by_id(self.cliente_id)
        if cliente:
            self.ui.lineEdit.setText(cliente.nombre)
            self.ui.lineEdit_2.setText(cliente.direccion)

    def obtener_datos(self):
        nombre = self.ui.lineEdit.text().strip().title()
        direccion = self.ui.lineEdit_2.text().strip().title()
        telefono = self.ui.lineEdit_3.text().strip().title()
        return(nombre, direccion, telefono)
    
    def guardar_cliente(self):
        nombre, direccion, telefono = self.obtener_datos()
        
        if not nombre or not direccion:
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Por favor, completa los campos obligatorios (nombre y dirección).")
            msg.exec()
            return
        if self.cliente_id:
            if Cliente.actualizar(self.cliente_id,nombre,direccion,telefono) == True:
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Exito")
                msg.setText("Cliente actualizado correctamente.")
                msg.exec()
        else:
            if Cliente.registrar(nombre,direccion,telefono) == True:
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Exito")
                msg.setText("Cliente registrado correctamente.")
                msg.exec()
        self.client_controller.mostrar_clientes()
        if self.caja_controller:
            self.caja_controller.clientes_combobox()
        self.ui.close() 
        self.limpiar_formulario()

    #def confirmar_eliminacion(self,respuesta,cliente_id):
    #    if respuesta == QMessageBox.StandardButton.Yes:
    #        if Cliente.eliminar_cliente(cliente_id) == True:
    #            msg=QMessageBox()
    #            msg.setIcon(QMessageBox.Icon.Information)
    #            msg.setWindowTitle("Eliminación")
    #            msg.setText("Cliente eliminado correctamente.")
    #            msg.exec()
    #            self.client_controller.mostrar_clientes()
       