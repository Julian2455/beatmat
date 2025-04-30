from gui.controller import *
from models import *
from utils import get_image
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QPixmap

class RecargaFormController(QDialog):
    def __init__(self,ui,extintor_controller, vencimientos_controller, recarga_id=None):
        super().__init__()
        self.ui = ui
        self.recarga_controller = extintor_controller
        self.vencimientos_controller = vencimientos_controller
        self.recarga_id = recarga_id
        self.ui.spinBox_vto_ph.setValue(QDate.currentDate().year())
        self.ui.spinBox_fabricacion.setValue(QDate.currentDate().year())
        self.ui.dateEdit_vto_control.setDate(QDate.currentDate())
        self.ui.dateEdit_nuevo_control.setDate(QDate.currentDate())
        if self.recarga_id: 
            self.cargar_datos_recarga()
        self.ui.cancelar_form.clicked.connect(self.cerrar_form)
        self.ui.guardar_recarga.clicked.connect(self.guardar_recarga)
        self.ui.label.setPixmap(QPixmap(get_image("extintor")))
    
    def cerrar_form(self):
        self.ui.close()
        self.ui.spinBox_vto_ph.setValue(QDate.currentDate().year())
        self.ui.spinBox_fabricacion.setValue(QDate.currentDate().year())
        self.ui.dateEdit_nuevo_control.setDate(QDate.currentDate())
        self.ui.dateEdit_vto_control.setDate(QDate.currentDate())
    
    def obtener_datos(self):
        vto_control=self.ui.dateEdit_vto_control.date()
        nuevo_control=self.ui.dateEdit_nuevo_control.date()
        vto_ph=self.ui.spinBox_vto_ph.value()
        fabricacion=self.ui.spinBox_fabricacion.value()
        vto_control=vto_control.toPyDate()
        nuevo_control=nuevo_control.toPyDate()
        return(vto_control,nuevo_control,vto_ph,fabricacion)
    
    def guardar_recarga(self):
        vto_control,nuevo_control,vto_ph,fabricacion=self.obtener_datos()
        extintor_id = self.ui.extintor_id 
        if Recarga.registrar(vto_control,nuevo_control,vto_ph,fabricacion,extintor_id):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Éxito")
            msg.setText("Recarga registrada correctamente.")
            msg.exec()
            self.recarga_controller.actualizar_tablas(self.ui.extintor_id)
            self.vencimientos_controller.mostrar_vencimientos()
            self.cerrar_form()