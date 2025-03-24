from gui.controller import *
from models import *
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from db import SessionLocal

class ClientFormController(QDialog):
    def __init__(self,ui,client_controller):
        super().__init__()
        self.ui = ui
        self.client_controller = client_controller

        self.ui.guardar_client.clicked.connect(self.registrar_cliente)
        self.ui.cancelar_form.clicked.connect(self.cerrar_form)
    
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
            QMessageBox.warning(self.ui, "Error", "Por favor, completa todos los campos.")
            return
        
        db=SessionLocal()
        try:
            nuevo_cliente = Cliente(nombre=nombre, direccion=direccion)
            db.add(nuevo_cliente)
            db.commit()
            QMessageBox.information(self.ui, "Éxito", "Cliente registrado correctamente.")

            self.client_controller.mostrar_clientes() 
        
        except Exception as e:
            db.rollback()
            print("Error al guardar cliente", e)

        finally:
            db.close()

        self.ui.close() 

        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        


