from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QMenu
from models import *
from utils import get_image
from PyQt6.QtGui import QIcon, QDoubleValidator, QPixmap
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

    def cancelar(self):
        self.ui.close()
        self.ui.lineEdit.clear()
    
    def limpiar_formulario(self):
        self.ui.lineEdit.clear()

    def mostrar_form(self, tipo):
        self.tipo_formulario = tipo
        self.ui.label_config.setText(f"Registrar {tipo}")
        self.ui.setWindowTitle(f"Registrar {tipo}")
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
        elif tipo == "Gastos":
            datos= CatGasto.show_all()
            self.ui.label_registro.setText(f"Categorias registradas")
        elif tipo == "Pagos":
            self.ui.label_config.setText(f"Registrar medio de pago")
            self.ui.setWindowTitle(f"Registrar medio de pago")
            datos= CatPagos.show_all()
            self.ui.label_registro.setText(f"Medios de pago registrados")
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
        nombre = self.ui.lineEdit.text().title()
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
        elif tipo == "Gastos":
            if CatGasto.registrar_categoria(nombre) == True:
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Exito")
                msg.setText(f"Categoria '{nombre}' registrada correctamente.")
                msg.exec()
                if self.gts_form_controller:
                    self.gts_form_controller.llenar_comboBox()
        elif tipo == "Pagos":
            if CatPagos.registrar_medio_pago(nombre) == True:
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Exito")
                msg.setText(f"Medio de pago '{nombre}' registrado correctamente.")
                msg.exec()
        self.caja_controller.pagos_combobox()
        self.extintor_controller.llenar_combobox_filtro()
        self.extintor_form_controller.llenar_combobox()
        #self.ui.close()
        self.limpiar_formulario()
        self.mostrar_form(self.tipo_formulario)

    
    def mostrar_menu_contextual(self, posicion):
        index = self.ui.tableWidget.indexAt(posicion)
        if not index.isValid():
            return
        fila = index.row()
        menu = QMenu()
        eliminar_action = menu.addAction("Eliminar")
        action = menu.exec(self.ui.tableWidget.mapToGlobal(posicion))
        if action == eliminar_action:
            self.eliminar_detalle(fila)
    def eliminar_detalle(self, row):
        tipo = self.tipo_formulario
        nombre = self.ui.tableWidget.item(row, 0).text()
        confirmar = QMessageBox.question(
            self.ui,
            "Eliminar",
            f"¿Estás seguro de que querés eliminar '{nombre}' de {tipo}s?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirmar == QMessageBox.StandardButton.No:
            return
        en_uso = False
        if tipo == "Marca":
            marca = Marca.get_by_nombre(nombre)
            if marca and marca.extintores:
                en_uso = True
            elif marca:
                Marca.eliminar_por_id(marca.id)
        elif tipo == "Tipo":
            tipo_obj = Tipo.get_by_nombre(nombre)
            if tipo_obj and tipo_obj.extintores:
                en_uso = True
            elif tipo_obj:
                Tipo.eliminar_por_id(tipo_obj.id)
        elif tipo == "Capacidad":
            cap = Capacidad.get_by_nombre(nombre)
            if cap and cap.extintores:
                en_uso = True
            elif cap:
                Capacidad.eliminar_por_id(cap.id)
        if en_uso:
            QMessageBox.warning(
                self.ui,
                "Elemento en uso",
                f"No se puede eliminar '{nombre}' porque está siendo utilizado por al menos un extintor."
            )
        else:
            QMessageBox.information(
                self.ui,
                "Eliminado",
                f"{tipo} '{nombre}' eliminado correctamente."
            )
        self.mostrar_form(self.tipo_formulario)
