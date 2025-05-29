from gui.controller import *
from models import *
from utils import get_image
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtGui import QPixmap,QRegularExpressionValidator
from PyQt6.QtCore import QDate, QRegularExpression

class GastosFormController(QDialog):
    def __init__(self,ui,gastos_controller,gasto_id=None):
        super().__init__()
        self.ui = ui
        self.gastos_controller = gastos_controller
        self.gasto_id = gasto_id 
        self.ui.dateEdit.setDate(QDate.currentDate())
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
    
    def obtener_datos(self):
        fecha=self.ui.dateEdit.date()
        fecha=fecha.toPyDate()
        insumo = self.ui.lineEdit.text()
        gasto = self.ui.lineEdit_3.text().replace(".", "")
        return(fecha,insumo, gasto)
    
    def guardar_gasto(self):
        fecha,insumo, gasto= self.obtener_datos()
        if Gastos.registrar(fecha,insumo,gasto):
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

