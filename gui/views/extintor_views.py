from PyQt6.QtWidgets import QWidget, QDialog
from gui.designer import Ui_Extintor, Ui_ExtintorDetails, Ui_ExtintorForm, Ui_TareasForm, Ui_RecargaForm, Ui_Impresion

class ExtintorUi(QWidget, Ui_Extintor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class ExtintorDetailsUi(QWidget, Ui_ExtintorDetails):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.extintor_id_actual = None 

class RegisterExtUi(QDialog, Ui_ExtintorForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    
    def mostrar_form(self):
        self.exec()

class TareaRegisterUi(QDialog, Ui_TareasForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.extintor_id = None
    
    def mostrar_form(self, extintor_id=None):
        self.extintor_id = extintor_id
        self.exec()

class RecargaRegisterUi(QDialog, Ui_RecargaForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.extintor_id = None
    
    def mostrar_form(self, extintor_id=None):
        self.extintor_id = extintor_id
        self.exec()

class ImpresionUi(QDialog, Ui_Impresion):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    
    def mostrar_form(self):
        self.exec()
