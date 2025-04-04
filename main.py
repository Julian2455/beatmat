from models import *
from gui.controller import *
from gui.designer import *

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
from PyQt6 import QtWidgets, QtCore

class ClientUi(QWidget, Ui_Client):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class ExtintorClientsDetailsUi(QWidget,Ui_ExtintorClientsDetails):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class RegisterClientUi(QDialog, Ui_ClientForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    def mostrar_form(self):
        self.exec()

class ExtintorUi(QWidget, Ui_Extintor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class ExtintorDetailsUi(QWidget, Ui_ExtintorDetails):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.extintor_id_actual = None 

class RegisterExtUi(QDialog, Ui_ExtintorForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    def mostrar_form(self):
        self.exec()

class TareaRegisterUi(QDialog, Ui_TareasForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.extintor_id = None
    def mostrar_form(self, extintor_id=None):
        self.extintor_id = extintor_id
        self.exec()

class RecargaRegisterUi(QDialog, Ui_RecargaForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.extintor_id = None
    def mostrar_form(self, extintor_id=None):
        self.extintor_id = extintor_id
        self.exec()

class CajaUi(QWidget,Ui_Caja):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class RegisterCajaui(QDialog, Ui_CajaForm):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
    def mostrar_form(self):
        self.exec()

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cliente_tab = ClientUi()
        self.cliente_extintor = ExtintorClientsDetailsUi()
        self.ui.Clientes.setLayout(QtWidgets.QVBoxLayout())
        self.ui.Clientes.layout().addWidget(self.cliente_tab)
        self.ui.Clientes.layout().addWidget(self.cliente_extintor)
        self.cliente_extintor.hide()
        self.client_controller = ClientController(self.cliente_tab)
        self.client_controller.asociacion_ui=self.cliente_extintor
        self.cliente_extintor.btnAtras.clicked.connect(self.show_clientes_tab)
        self.alta_client = RegisterClientUi()
        self.cliente_tab.pushButton_5.clicked.connect(self.alta_client.mostrar_form)
        self.client_form_controller = ClientFormController(self.alta_client, self.client_controller)
        self.edit_client = RegisterClientUi()
        self.client_controller.set_edit_form_cli(self.edit_client)
        self.edit_client_controller = ClientFormController(self.edit_client, self.client_controller)
        self.client_controller.edit_client_controller = self.edit_client_controller
        self.setWindowTitle("LE * LO Matafuegos")
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.matafuegos_container = QtWidgets.QWidget()
        self.matafuegos_layout = QtWidgets.QVBoxLayout(self.matafuegos_container)
        self.extintor_tab = ExtintorUi()
        self.extintor_details_tab = ExtintorDetailsUi()
        self.matafuegos_layout.addWidget(self.extintor_tab)
        self.matafuegos_layout.addWidget(self.extintor_details_tab)
        self.scroll_area.setWidget(self.matafuegos_container)
        self.ui.Matafuegos.setLayout(QtWidgets.QVBoxLayout())
        self.ui.Matafuegos.layout().addWidget(self.scroll_area)
        self.extintor_details_tab.hide()
        self.extintor_controller = ExtintorController(self.extintor_tab)
        self.extintor_controller.details_ui = self.extintor_details_tab
        self.alta_extintor = RegisterExtUi()
        self.extintor_tab.pushButton_5.clicked.connect(self.alta_extintor.mostrar_form)
        self.extintor_form_controller = ExtFormController(self.alta_extintor, self.extintor_controller)
        self.extintor_details_tab.btnAtras.clicked.connect(self.show_extintor_tab)
        self.edit_extintor = RegisterExtUi()
        self.extintor_controller.set_edit_form_ext(self.edit_extintor)
        self.edit_extintor_controller = ExtFormController(self.edit_extintor, self.extintor_controller)
        self.extintor_controller.edit_extintor_controller = self.edit_extintor_controller
        self.alta_tarea = TareaRegisterUi()
        self.extintor_details_tab.btnAgregarTareas.clicked.connect(self.mostrar_form_tarea)
        self.tarea_form_controller = TareaFormController(self.alta_tarea, self.extintor_controller)
        self.alta_recarga = RecargaRegisterUi()
        self.extintor_details_tab.btnAgregarRecarga.clicked.connect(self.mostrar_form_recarga)
        self.recarga_form_controller = RecargaFormController(self.alta_recarga, self.extintor_controller)
        self.caja_tab = CajaUi()
        self.caja_controller = CajaController(self.caja_tab)
        self.ui.Caja.setLayout(QtWidgets.QVBoxLayout())
        self.ui.Caja.layout().addWidget(self.caja_tab)
        self.alta_caja = RegisterCajaui()
        self.caja_tab.abrir_caja.clicked.connect(self.alta_caja.mostrar_form)
    
    def show_extintor_tab(self):
        self.extintor_details_tab.hide()   
        self.extintor_tab.show()
    
    def show_clientes_tab(self):
        self.cliente_extintor.hide()
        self.cliente_tab.show()
    
    def mostrar_form_tarea(self):
        extintor_id = self.extintor_details_tab.extintor_id_actual
        self.alta_tarea.mostrar_form(extintor_id)
    
    def mostrar_form_recarga(self):
        extintor_id = self.extintor_details_tab.extintor_id_actual
        self.alta_recarga.mostrar_form(extintor_id)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())