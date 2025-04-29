from PyQt6.QtWidgets import QLabel, QHBoxLayout, QLineEdit, QMessageBox
from models import *
from utils import get_image
from PyQt6.QtGui import QIcon, QDoubleValidator
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QObject, QLocale

class PricesController(QObject):
    def __init__(self,ui):
        super().__init__()
        self.ui = ui
        self.formato_decimales()
        self.cargar_precio_nuevos()
        self.cargar_precio_recargas()
        self.ui.btnGuardar.clicked.connect(self.guardar_cambios)
        self.ui.btnCancelar.clicked.connect(self.cancelar_cambios)

    def formato_decimales(self):
        self.validator = QDoubleValidator()
        self.validator.setDecimals(2)
        self.validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.locale = QLocale(QLocale.Language.Spanish)
        self.locale.setNumberOptions(QLocale.NumberOption.OmitGroupSeparator)
        self.validator.setLocale(self.locale)

    def cargar_precio_nuevos(self):
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
                print(cambios)
                QMessageBox.information(self.ui, "Éxito", "Los precios se han actualizado correctamente.")
                for id_precio, datos in cambios.items():
                    if datos['tipo'] == 'recarga': #Ver como funciona esta forma, si no cambiar por consulta/restaurar y llamar al metodo otra vez
                        self.line_edits_recargas[id_precio].setProperty("valor_original", datos['valor'])
                        self.line_edits_recargas[id_precio].setText(self.locale.toString(float(datos['valor']), 'f', 2))
                        self.line_edits_recargas[id_precio].setStyleSheet("background-color: white;")
                    else:
                        self.line_edits_nuevos[id_precio].setProperty("valor_original", datos['valor'])
                        self.line_edits_nuevos[id_precio].setText(self.locale.toString(float(datos['valor']), 'f', 2))
                        self.line_edits_nuevos[id_precio].setStyleSheet("background-color: white;")
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