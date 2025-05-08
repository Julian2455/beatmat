from PyQt6.QtWidgets import QMainWindow, QScrollArea
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon

from gui.designer import Ui_MainWindow
from gui.views import *
from gui.controller import *
from utils import get_image

class MainController:
    def __init__(self):
        self.ventana = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.ventana)
        
        # Iniciar componentes
        self.init_prices_bar()
        self.init_clientes_tab()
        self.init_extintores_tab()
        self.init_mtc_bar()
        self.init_caja_tab()
        self.init_vencimientos_tab() 
        
        # Configurar iconos para las tabs
        self.setup_tab_icons()
        
        # Poner nombre en la ventana
        self.ventana.setWindowTitle("LE * LO Matafuegos")
    
    def init_clientes_tab(self):
        # Configurar la tab de clientes
        self.cliente_tab = ClientUi()
        self.cliente_extintor = ExtintorClientsDetailsUi()
        self.ui.Clientes.setLayout(QtWidgets.QVBoxLayout())
        self.ui.Clientes.layout().addWidget(self.cliente_tab)
        self.ui.Clientes.layout().addWidget(self.cliente_extintor)
        self.cliente_extintor.hide()
        
        # Conectar controladores
        self.client_controller = ClientController(self.cliente_tab)
        self.client_controller.asociacion_ui = self.cliente_extintor
        self.cliente_extintor.btnAtras.clicked.connect(self.show_clientes_tab)
        
        # Formularios para alta y edicion de clientes
        self.alta_client = RegisterClientUi()
        self.cliente_tab.pushButton_5.clicked.connect(self.alta_client.mostrar_form)
        self.client_form_controller = ClientFormController(self.alta_client, self.client_controller)
        
        self.edit_client = RegisterClientUi()
        self.client_controller.set_edit_form_cli(self.edit_client)
        self.edit_client_controller = ClientFormController(self.edit_client, self.client_controller)
        self.client_controller.edit_client_controller = self.edit_client_controller
    
    def init_extintores_tab(self):
        # Configurar la tab de matafuegos
        self.scroll_area = QScrollArea()
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
        
        # Conectar controladores
        self.extintor_controller = ExtintorController(self.extintor_tab)
        self.extintor_controller.details_ui = self.extintor_details_tab
        self.extintor_details_tab.btnAtras.clicked.connect(self.show_extintor_tab)
        
        # Formularios para alta y edicion de extintores
        self.alta_extintor = RegisterExtUi()
        self.extintor_tab.pushButton_5.clicked.connect(self.alta_extintor.mostrar_form)
        self.extintor_form_controller = ExtFormController(self.alta_extintor, self.extintor_controller, precios_controller=self.precios_controller)
        
        self.edit_extintor = RegisterExtUi()
        self.extintor_controller.set_edit_form_ext(self.edit_extintor)
        self.edit_extintor_controller = ExtFormController(self.edit_extintor, self.extintor_controller, precios_controller=self.precios_controller)
        self.extintor_controller.edit_extintor_controller = self.edit_extintor_controller
        
        # Formularios para tareas y recargas
        self.alta_tarea = TareaRegisterUi()
        self.extintor_details_tab.btnAgregarTareas.clicked.connect(self.mostrar_form_tarea)
        self.tarea_form_controller = TareaFormController(self.alta_tarea, self.extintor_controller)
        
        self.alta_recarga = RecargaRegisterUi()
        self.extintor_details_tab.btnAgregarRecarga.clicked.connect(self.mostrar_form_recarga)
        self.recarga_form_controller = RecargaFormController(self.alta_recarga, self.extintor_controller, None)
    
    def init_caja_tab(self):
        # Configurar la tab de caja
        self.caja_tab = CajaUi()
        self.caja_controller = CajaController(self.caja_tab)
        self.ui.Caja.setLayout(QtWidgets.QVBoxLayout())
        self.ui.Caja.layout().addWidget(self.caja_tab)
        
        # Ventana para agregar extintores
        self.agregar_extintor = AgregarExtintorUi()
        self.caja_tab.btnAgregarExtintores.clicked.connect(self.mostrar_form_agregarext)
        self.agregar_extintor_controller = None

        # Conexion para cargar clientes desde la tab de caja
        self.caja_tab.btnNuevoCliente.clicked.connect(self.alta_client.mostrar_form)
        self.client_form_controller = ClientFormController(self.alta_client, self.client_controller, caja_controller=self.caja_controller)
        # Conexion para cargar extintores desde el formulario en la tab de caja
        self.agregar_extintor.btnNuevoExtintor.clicked.connect(self.alta_extintor.mostrar_form)
        #self.extintor_form_controller = ExtFormController(self.alta_extintor, self.extintor_controller, agregar_extintor_controller=self.agregar_extintor_controller)
    
    def init_prices_bar(self):
        # Instancia de PreciosUi y conexion con el formulario
        self.precios_ui = PreciosUi()
        self.precios_controller = PricesController(self.precios_ui)
        self.ui.actionPrecios.triggered.connect(self.mostrar_form_precios)

    def init_mtc_bar(self):
        self.config_form = ConfigUi()
        self.mtc_controller = MtcController(self.config_form, self.extintor_controller)
        self.ui.actionMarcas.triggered.connect(lambda: self.mostrar_form_universal("Marca"))
        self.ui.actionTipos.triggered.connect(lambda: self.mostrar_form_universal("Tipo"))
        self.ui.actionCapacidad.triggered.connect(lambda: self.mostrar_form_universal("Capacidad"))

    #PARTE DE VENCIMIENTOS 
    def init_vencimientos_tab(self):
        self.vencimientos_tab=VencimientosUi()
        self.ui.Vencimientos.setLayout(QtWidgets.QVBoxLayout())
        self.ui.Vencimientos.layout().addWidget(self.vencimientos_tab)

        #conectar controladores
        self.vencimientos_controller=VencimientosController(self.vencimientos_tab)
        self.recarga_form_controller.vencimientos_controller = self.vencimientos_controller

    def setup_tab_icons(self):
        # Reconfigurar iconos en las tabs para el ejecutable
        self.ui.tabWidget.setTabIcon(0, QIcon(get_image("avatar")))
        self.ui.tabWidget.setTabIcon(1, QIcon(get_image("extintor-de-incendios(1)")))
        self.ui.tabWidget.setTabIcon(2, QIcon(get_image("salario")))
        self.ui.tabWidget.setTabIcon(3, QIcon(get_image("estadisticas")))
        self.ui.tabWidget.setTabIcon(4, QIcon(get_image("fecha_de_vencimiento")))
    
    def show_extintor_tab(self):
        # Alternar contenido/detalles
        self.extintor_details_tab.hide()
        self.extintor_tab.show()
    
    def show_clientes_tab(self):
        # Alternar contenido/detalles
        self.cliente_extintor.hide()
        self.cliente_tab.show()
    
    def show_vencimientos_tab(self):
        #Alternas contenido/detalles
        self.vencimientos_details.hide()
        self.vencimientos_tab.show()
    
    def mostrar_form_tarea(self):
        extintor_id = self.extintor_details_tab.extintor_id_actual
        self.alta_tarea.mostrar_form(extintor_id)
    
    def mostrar_form_recarga(self):
        extintor_id = self.extintor_details_tab.extintor_id_actual
        self.alta_recarga.mostrar_form(extintor_id)
    
    def mostrar_form_agregarext(self):
        cliente_id = self.caja_tab.cliente_id_actual
        if cliente_id is None:
            return
        if self.agregar_extintor_controller is None:
            self.agregar_extintor_controller = CajaFormController(self.agregar_extintor, self.caja_controller, cliente_id)
        else:
            self.agregar_extintor_controller.reiniciar(cliente_id)    
        self.extintor_form_controller = ExtFormController(self.alta_extintor, self.extintor_controller, agregar_extintor_controller=self.agregar_extintor_controller)        
        self.agregar_extintor.mostrar_form()
    
    def mostrar_form_precios(self):
        self.precios_ui.mostrar_form()

    def mostrar_form_universal(self, tipo):
        self.mtc_controller.mostrar_form(tipo)
    
    def show(self):
        self.ventana.show()