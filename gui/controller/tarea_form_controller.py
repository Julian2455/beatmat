from gui.controller import *
from models import *
from utils import get_image
from PyQt6.QtWidgets import QDialog, QMessageBox, QCheckBox
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QPixmap

class TareaFormController(QDialog):
    def __init__(self, ui, extintor_controller, tarea_id=None):
        super().__init__()
        self.ui = ui
        self.tarea_controller = extintor_controller
        self.tarea_id = tarea_id
        self.ui.dateEdit_fecha.setDate(QDate.currentDate())
        if self.tarea_id: 
            self.cargar_datos_tarea()
        self.ui.cancelar_form.clicked.connect(self.cerrar_form)
        self.ui.guardar_tareas.clicked.connect(self.guardar_tarea)
        self.ui.label.setPixmap(QPixmap(get_image("extintor")))
        self.aplicar_estilo_checkboxes() 

    def aplicar_estilo_checkboxes(self):
        estilo_checkbox = """
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:checked {
                background-color: #2C3E50;
                border: 1px solid #2C3E50;
            }
            QCheckBox::indicator:unchecked {
                background-color: white;
                border: 1px solid #2C3E50;
            }
        """
        checkboxes = [
            self.ui.checkBox_bastago_bronce,
            self.ui.checkBox_cambio_manometro,
            self.ui.checkBox_control_tacho,
            self.ui.checkBox_gatillo,
            self.ui.checkBox_interior,
            self.ui.checkBox_oring,
            self.ui.checkBox_otro,
            self.ui.checkBox_peso,
            self.ui.checkBox_pintura,
            self.ui.checkBox_relleno_polvo,
            self.ui.checkBox_tamizacion,
            self.ui.checkBox_valvula,
            self.ui.checkBox_ph,
            self.ui.checkBox_manguera
        ]
        for checkbox in checkboxes:
            checkbox.setStyleSheet(estilo_checkbox)

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
        self.ui.checkBox_ph.setChecked(False)
        self.ui.checkBox_manguera.setChecked(False)
        self.ui.lineEditEmpresa.clear()
        self.ui.textEdit_observacion.clear()
        self.ui.dateEdit_fecha.setDate(QDate.currentDate())

    def obtener_datos(self):
        bastago = self.ui.checkBox_bastago_bronce.isChecked()
        manometro = self.ui.checkBox_cambio_manometro.isChecked()
        tacho = self.ui.checkBox_control_tacho.isChecked()
        gatillo = self.ui.checkBox_gatillo.isChecked()
        interior = self.ui.checkBox_interior.isChecked()
        oring = self.ui.checkBox_oring.isChecked()
        otro = self.ui.checkBox_otro.isChecked()
        peso = self.ui.checkBox_peso.isChecked()
        pintura = self.ui.checkBox_pintura.isChecked()
        relleno = self.ui.checkBox_relleno_polvo.isChecked()
        tamizacion = self.ui.checkBox_tamizacion.isChecked()
        valvula = self.ui.checkBox_valvula.isChecked()
        manguera = self.ui.checkBox_manguera.isChecked()
        ph = self.ui.checkBox_ph.isChecked()
        empresa = self.ui.lineEditEmpresa.text()
        observacion = self.ui.textEdit_observacion.toPlainText()
        fecha = self.ui.dateEdit_fecha.date().toPyDate()

        return (
            bastago, manometro, tacho, gatillo, interior,
            oring, otro, peso, pintura, relleno,
            tamizacion, valvula, manguera, ph, empresa, observacion, fecha
        )

    def guardar_tarea(self):
        bastago, manometro, tacho, gatillo, interior, oring, otro, peso, pintura, relleno, tamizacion, valvula, manguera, ph, empresa, observacion, fecha = self.obtener_datos()
        extintor_id = self.ui.extintor_id
        if Tareas.registrar(
            bastago, manometro, tacho, gatillo, interior,
            oring, otro, peso, pintura, relleno,
            tamizacion, valvula, manguera, ph, empresa, observacion, fecha, extintor_id
        ):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Éxito")
            msg.setText("Tarea registrada correctamente.")
            msg.exec()
            self.tarea_controller.actualizar_tablas(extintor_id)
            self.cerrar_form()
