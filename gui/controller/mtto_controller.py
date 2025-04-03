from gui.controller import *
from models import *
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QDate

class TareaFormController(QDialog):
    def __init__(self,ui,extintor_controller, tarea_id=None):
        super().__init__()
        self.ui = ui
        self.tarea_controller = extintor_controller
        self.tarea_id = tarea_id
        self.ui.dateEdit_fecha.setDate(QDate.currentDate())
        if self.tarea_id: 
            self.cargar_datos_tarea()
        self.ui.cancelar_form.clicked.connect(self.cerrar_form)
    

    def cerrar_form(self):
        self.ui.close()
        self.ui.checkBox_bastago_bronce.setChecked(False)
        self.ui.checkBox_cambio_manometro.setChecked(False)
        self.ui.checkBox_control_tacho.setChecked(False)
        self.ui.checkBox_gatillo.setChecked(False)
        self.ui.checkBox_interior.setChecked(False)
        self.ui.checkBox_oring.setChecked(False)
        self.ui.checkBox_otro.setChecked(False)
        self.ui.checkBox_peso.setChecked(False)
        self.ui.checkBox_pintura.setChecked(False)
        self.ui.checkBox_relleno_polvo.setChecked(False)
        self.ui.checkBox_tamizacion.setChecked(False)
        self.ui.checkBox_valvula.setChecked(False)
        self.ui.textEdit_observacion.clear()
        self.ui.dateEdit_fecha.setDate(QDate.currentDate())

        self.extintor_id = None