from gui.controller import *
from models import *
from utils import get_image
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtGui import QPixmap,QRegularExpressionValidator
from PyQt6.QtCore import QDate, QRegularExpression
from PyQt6 import QtCore

class GastosFormController(QDialog):
    def __init__(self,ui,gastos_controller,gasto_id=None):
        super().__init__()
        self.ui = ui
        self.gastos_controller = gastos_controller
        self.gasto_id = gasto_id 
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.llenar_comboBox()
        self.ui.guardar_gasto.clicked.connect(self.guardar_gasto)
        self.ui.cancelar_form.clicked.connect(self.cerrar_form)
        self.ui.label.setPixmap(QPixmap(get_image("dinero")))
        solo_numeros_validator = QRegularExpressionValidator(QRegularExpression(r"\d+"))
        self.ui.lineEdit_3.setValidator(solo_numeros_validator)
        self.ui.lineEdit_3.textChanged.connect(self.formatear_gasto)

    def cerrar_form(self):
        self.ui.close()
        self.ui.lineEdit.clear()
        self.ui.lineEdit_3.clear()
    
    def limpiar_formulario(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_3.clear()
        self.ui.comboBox_categoria.clear()
    
    def llenar_comboBox(self):
        self.ui.comboBox_categoria.clear()
        self.ui.comboBox_categoria.addItem("Seleccionar categoría...")
        lista=CatGasto.show_all()
        for categoria in lista:
            self.ui.comboBox_categoria.addItem(categoria.nombre)
            index=self.ui.comboBox_categoria.count()-1
            self.ui.comboBox_categoria.setItemData(index, categoria.id, QtCore.Qt.ItemDataRole.UserRole)
    
    def obtener_datos(self):
        fecha=self.ui.dateEdit.date()
        fecha=fecha.toPyDate()
        insumo = self.ui.lineEdit.text()
        gasto = self.ui.lineEdit_3.text().replace(".", "")
        categoria=self.ui.comboBox_categoria.currentData(QtCore.Qt.ItemDataRole.UserRole)
        return(fecha,insumo, gasto, categoria)
    
    def guardar_gasto(self):
        fecha,insumo, gasto, categoria= self.obtener_datos()
        if not fecha or not insumo or not gasto or not categoria:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Por favor, completa todos los campos.")
            msg.exec()
            return
        else: 
            Gastos.registrar(fecha,insumo,gasto,categoria)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Éxito")
            msg.setText("Gasto registrado correctamente.")
            msg.exec()
            self.gastos_controller.mostrar_gastos()
            self.cerrar_form()
            self.limpiar_formulario()

    def formatear_gasto(self):
        texto = self.ui.lineEdit_3.text()
        texto_limpio = texto.replace(".", "")
        if not texto_limpio:
            return
        try:
            numero = int(texto_limpio)
            texto_formateado = f"{numero:,}".replace(",", ".")
            self.ui.lineEdit_3.blockSignals(True)
            self.ui.lineEdit_3.setText(texto_formateado)
            self.ui.lineEdit_3.blockSignals(False)
        except ValueError:
            pass

