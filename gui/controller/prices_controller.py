from PyQt6.QtWidgets import QLabel, QHBoxLayout, QLineEdit, QMessageBox, QVBoxLayout, QWidget
from models import *
from utils import get_image
from PyQt6.QtGui import QIcon, QDoubleValidator, QPixmap
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QObject, QLocale

class PricesController(QObject):
    def __init__(self,ui,config_controller, extintor_controller):
        super().__init__()
        self.ui = ui
        self.config_controller = config_controller
        self.extintor_controller = extintor_controller
        self.tipo_formulario = None
        self.formato_decimales()
        self.cargar_precio_nuevos()
        self.cargar_precio_recargas()
        self.ui.btnGuardar.clicked.connect(self.guardar_cambios)
        self.ui.btnCancelar.clicked.connect(self.cancelar_cambios)
        self.config_controller.guardar_detalle.clicked.connect(self.guardar_detalle)
        self.config_controller.cancelar_form.clicked.connect(self.cancelar)
        self.config_controller.label.setPixmap(QPixmap(get_image("config2")))

    def formato_decimales(self):
        self.validator = QDoubleValidator()
        self.validator.setDecimals(2)
        self.validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.locale = QLocale(QLocale.Language.Spanish)
        self.locale.setNumberOptions(QLocale.NumberOption.OmitGroupSeparator)
        self.validator.setLocale(self.locale)

    def cargar_precio_nuevos(self):
        self.limpiar_layout(self.ui.verticalLayoutNuevos)
        tipos = Precios.precio_nuevos()
        self.line_edits_nuevos = {}  
        for listado in tipos:
            hbox = QHBoxLayout()
            labeldata = QLabel()
            labeldata.setText(f'{listado.marca} {listado.tipo} {listado.capacidad}')
            labeldata.setStyleSheet("border: none;")
            lineEditPrecio = QLineEdit()
            lineEditPrecio.setValidator(self.validator)
            lineEditPrecio.setText(self.locale.toString(float(listado.valor), 'f', 2))
            lineEditPrecio.setStyleSheet("background-color: white;")
            lineEditPrecio.setProperty("id", listado.id)
            lineEditPrecio.setProperty("valor_original", listado.valor)
            lineEditPrecio.textChanged.connect(self.resaltar_campo_modificado)
            self.line_edits_nuevos[listado.id] = lineEditPrecio
            hbox.addWidget(labeldata)
            hbox.addStretch()
            hbox.addWidget(lineEditPrecio)
            self.ui.verticalLayoutNuevos.addLayout(hbox)
        self.ui.verticalLayoutNuevos.addStretch()
    
    def cargar_precio_recargas(self):
        self.limpiar_layout(self.ui.verticalLayoutRecargas)
        tipos = Precios.precio_recargas()
        self.line_edits_recargas = {} 
        for listado in tipos:
            hbox = QHBoxLayout()
            labeldata = QLabel()
            labeldata.setText(f'{listado.capacidad}')
            labeldata.setStyleSheet("border: none;")
            lineEditPrecio = QLineEdit()
            lineEditPrecio.setValidator(self.validator)
            lineEditPrecio.setText(self.locale.toString(float(listado.valor), 'f', 2))
            lineEditPrecio.setStyleSheet("background-color: white;")
            lineEditPrecio.setProperty("id", listado.id)
            lineEditPrecio.setProperty("valor_original", listado.valor)
            lineEditPrecio.textChanged.connect(self.resaltar_campo_modificado)
            self.line_edits_recargas[listado.id] = lineEditPrecio
            hbox.addWidget(labeldata)
            hbox.addStretch()
            hbox.addWidget(lineEditPrecio)
            self.ui.verticalLayoutRecargas.addLayout(hbox)
        self.ui.verticalLayoutRecargas.addStretch()
    
    def resaltar_campo_modificado(self):
        sender = self.sender()
        if not sender:
            return
        valor_original = sender.property("valor_original")
        try:
            valor_actual = self.locale.toDouble(sender.text())[0] 
            if abs(valor_actual - valor_original) > 0.001:
                sender.setStyleSheet("background-color: #FFFACD;")
            else:
                sender.setStyleSheet("background-color: white;")
        except Exception:
            sender.setStyleSheet("background-color: white;")

    def guardar_cambios(self):
        cambios = {}
        for id_precio, line_edit in self.line_edits_recargas.items():
            valor_original = line_edit.property("valor_original")
            try:
                valor_actual = self.locale.toDouble(line_edit.text())[0]
                if abs(valor_actual - valor_original) > 0.001:
                    cambios[id_precio] = {'valor': valor_actual, 'tipo': 'recarga'}
            except Exception:
                pass
        for id_precio, line_edit in self.line_edits_nuevos.items():
            valor_original = line_edit.property("valor_original")
            try:
                valor_actual = self.locale.toDouble(line_edit.text())[0]
                if abs(valor_actual - valor_original) > 0.001:
                    cambios[id_precio] = {'valor': valor_actual, 'tipo': 'nuevo'}
            except Exception:
                pass
        if cambios:
            try:
                Precios.actualizar_precios(cambios)
                QMessageBox.information(self.ui, "Éxito", "Los precios se han actualizado correctamente.")
                self.cargar_precio_recargas()
                self.cargar_precio_nuevos()
            except Exception as e:
                QMessageBox.critical(self.ui, "Error", f"No se pudieron guardar los cambios: {str(e)}")
        else:
            QMessageBox.information(self.ui, "Información", "No se detectaron cambios en los precios.")
    
    def cancelar_cambios(self):
        for id_precio, line_edit in self.line_edits_recargas.items():
            valor_original = line_edit.property("valor_original")
            line_edit.setText(self.locale.toString(float(valor_original), 'f', 2))
            line_edit.setStyleSheet("background-color: white;")

        for id_precio, line_edit in self.line_edits_nuevos.items():
            valor_original = line_edit.property("valor_original")
            line_edit.setText(self.locale.toString(float(valor_original), 'f', 2))
            line_edit.setStyleSheet("background-color: white;")
        QMessageBox.information(self.ui, "Información", "Se han descartado los cambios.")

    def limpiar_layout(self, layout):
        """Elimina todos los widgets y layouts hijos del layout proporcionado"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                child_layout = item.layout()
                if child_layout is not None:
                    self.limpiar_layout(child_layout)
                    child_layout.deleteLater()
    
    """Empieza la parte de registrar marcas, tipos y capacidades"""
    def cancelar(self):
        self.config_controller.close()
        self.config_controller.lineEdit.clear()
    
    def limpiar_formulario(self):
        self.config_controller.lineEdit.clear()

    def mostrar_formulario_universal(self, tipo):
        self.tipo_formulario = tipo
        self.config_controller.label_config.setText(f" {tipo}")
        self.config_controller.nombre_detalle.setText(f"{tipo}")
        self.config_controller.show()
    
    def guardar_detalle(self):
        tipo = self.tipo_formulario
        nombre = self.config_controller.lineEdit.text().strip().title()
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
                msg.setText("Marca registrada correctamente.")
                msg.exec()
        elif tipo == "Tipo":
            if Tipo.registrar_tipo(nombre) == True:
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Exito")
                msg.setText("Tipo registrado correctamente.")
                msg.exec()
        elif tipo == "Capacidad":
            if Capacidad.registrar_capacidad(nombre) == True:
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Exito")
                msg.setText("Capacidad registrada correctamente.")
                msg.exec()
        self.extintor_controller.llenar_combobox_filtro()
        self.config_controller.close()
        self.limpiar_formulario()