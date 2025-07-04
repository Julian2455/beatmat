from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QMenu
from models import *
from utils import get_image
from PyQt6.QtGui import QIcon, QDoubleValidator, QPixmap, QAction
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QObject, QLocale

class MtcController(QObject):
    def __init__(self,ui, extintor_controller,caja_controller, extintor_form_controller,gts_form_controller=None):
        super().__init__()
        self.ui = ui
        self.extintor_controller = extintor_controller
        self.caja_controller = caja_controller
        self.extintor_form_controller = extintor_form_controller
        self.gts_form_controller=gts_form_controller
        self.tipo_formulario = None
        self.ui.guardar_detalle.clicked.connect(self.guardar_detalle)
        self.ui.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.tableWidget.customContextMenuRequested.connect(self.mostrar_menu_contextual)
        self.ui.cancelar_form.clicked.connect(self.cancelar)
        self.ui.label.setPixmap(QPixmap(get_image("config2")))
        self.MODEL_DATA = {
        "Marca": {"model": Marca, "plural_label": "Marcas", "register_method_name": "registrar"},
        "Tipo": {"model": Tipo, "plural_label": "Tipos", "register_method_name": "registrar"},
        "Capacidad": {"model": Capacidad, "plural_label": "Capacidades", "register_method_name": "registrar"},
        "Gastos": {"model": CatGasto, "plural_label": "Categorías", "register_method_name": "registrar"},
        "Pagos": {"model": CatPagos, "plural_label": "Medios de pago", "register_method_name": "registrar", "form_title": "Registrar medio de pago"},
    }

    def cancelar(self):
        self.ui.close()
        self.ui.lineEdit.clear()
    
    def limpiar_formulario(self):
        self.ui.lineEdit.clear()
    
    def mostrar_mensaje(self, icon, title, text):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec()

    def mostrar_form(self, tipo):
        self.tipo_formulario = tipo
        model_data = self.MODEL_DATA.get(tipo)
        self.ui.label_config.setText(model_data.get("form_title", f"Registrar {tipo}"))
        self.ui.setWindowTitle(model_data.get("form_title", f"Registrar {tipo}"))
        self.ui.nombre_detalle.setText(f"{tipo}")
        self.ui.label_registro.setText(f"{model_data['plural_label']} registradas")
        datos = model_data["model"].show_all()
        self.ui.tableWidget.setRowCount(len(datos))
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.horizontalHeader().setVisible(False)
        for index, dato in enumerate(datos):
            id_nombre = QTableWidgetItem(str(dato.nombre))
            id_nombre.setData(Qt.ItemDataRole.UserRole, dato.id)
            self.ui.tableWidget.setItem(index, 0, id_nombre)
        self.ui.show()
        
    def guardar_detalle(self):
        tipo = self.tipo_formulario
        nombre = self.ui.lineEdit.text().title()
        if not nombre or not tipo:
            self.mostrar_mensaje(QMessageBox.Icon.Warning, "Error", f"Por favor, completa el campo de {tipo}. Es obligatorio.")
            return
        model_data = self.MODEL_DATA.get(tipo)
        model_class = model_data["model"]
        register_method = getattr(model_class, model_data["register_method_name"])
        if register_method(nombre):
            mensaje_exito = f"{model_data['plural_label']} '{nombre}' registrada correctamente."
            self.mostrar_mensaje(QMessageBox.Icon.Information, "Éxito", mensaje_exito)
            if tipo == "Gastos" and self.gts_form_controller:
                self.gts_form_controller.llenar_comboBox()
        else:
            self.mostrar_mensaje(QMessageBox.Icon.Warning, "Error", f"No se pudo registrar {model_data['plural_label']} '{nombre}'.")
        self.caja_controller.pagos_combobox()
        self.extintor_controller.llenar_combobox_filtro()
        self.extintor_form_controller.llenar_combobox()
        self.limpiar_formulario()
        self.mostrar_form(self.tipo_formulario)

    def obtener_id(self):
        item_seleccionado = self.ui.tableWidget.currentItem()
        if item_seleccionado:
            return item_seleccionado.data(Qt.ItemDataRole.UserRole)
        return None
    
    def mostrar_menu_contextual(self, pos):
        index = self.ui.tableWidget.indexAt(pos)
        if not index.isValid():
            return
        menu = QMenu(self.ui.tableWidget)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #CCCCCC;
            }
            QMenu::item {
                padding: 5px 15px;
                background-color: white;
            }
            QMenu::item:selected {
                background-color: #E0E0E0;
                color: black;
            }
        """)
        eliminar_action = QAction("Eliminar", self.ui.tableWidget)
        eliminar_action.triggered.connect(self.eliminar_detalle)
        menu.addAction(eliminar_action)
        menu.popup(self.ui.tableWidget.viewport().mapToGlobal(pos))

    def eliminar_detalle(self):
        item_seleccionado = self.ui.tableWidget.currentItem()
        id_a_eliminar = self.obtener_id()
        if id_a_eliminar is None:
            self.mostrar_mensaje(QMessageBox.Icon.Warning, "Advertencia", "No se pudo obtener el ID del elemento seleccionado.")
            return
        nombre = item_seleccionado.text()
        tipo = self.tipo_formulario
        model_data = self.MODEL_DATA.get(tipo)
        confirmar = QMessageBox.question(
            self.ui,
            "Eliminar",
            f"¿Estás seguro de que querés eliminar '{nombre}' de {model_data['plural_label']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirmar == QMessageBox.StandardButton.No:
            return
        model_class = model_data["model"]
        if model_class.eliminar_por_id(id_a_eliminar):
            self.mostrar_mensaje(QMessageBox.Icon.Information, "Eliminado", f"{tipo} '{nombre}' eliminado correctamente.")
        else:
            self.mostrar_mensaje(
                QMessageBox.Icon.Warning,
                "Elemento en uso",
                f"No se puede eliminar '{nombre}' porque está siendo utilizado por otros registros (ej. extintores o precios)."
            )
        self.mostrar_form(self.tipo_formulario)