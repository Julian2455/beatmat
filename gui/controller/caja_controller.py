from PyQt6.QtWidgets import QTableWidgetItem
from models import *
from utils import get_image
from PyQt6.QtGui import QIcon

class CajaController:
    def __init__(self,ui):
        self.ui = ui
        self.pagina_actual = 1 
        self.filas_por_pagina = 10  
        self.total_cajas = Caja.contar_cajas()
        self.total_paginas = (self.total_cajas // self.filas_por_pagina) + (1 if self.total_cajas % self.filas_por_pagina else 0)
        self.mostrar_cajas()
        self.ui.pushButton_2.clicked.connect(self.pagina_anterior) 
        self.ui.pushButton.clicked.connect(self.pagina_siguiente) 
        self.ui.pushButton_3.clicked.connect(self.primer_pagina) 
        self.ui.pushButton_4.clicked.connect(self.ultima_pagina) 
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.pushButton.setIcon(QIcon(get_image("sssiguiente"))) 
        self.ui.pushButton_2.setIcon(QIcon(get_image("anterior"))) 
        self.ui.pushButton_3.setIcon(QIcon(get_image("anterior_1"))) 
        self.ui.pushButton_4.setIcon(QIcon(get_image("proximo_1"))) 
    
    def mostrar_cajas(self):
        cajas = Caja.show_all(page=self.pagina_actual, per_page=self.filas_por_pagina)
        self.ui.tableWidget.setRowCount(len(cajas))
        for index, cajas in enumerate(cajas):
            pass

        self.actualizar_estado_paginado()

    def actualizar_estado_paginado(self):
        self.total_cajas = Caja.contar_cajas()
        self.total_paginas = (self.total_cajas // self.filas_por_pagina) + (1 if self.total_cajas % self.filas_por_pagina else 0)
        self.ui.label_7.setText(f"Página {self.pagina_actual} de {self.total_paginas}")
        self.ui.label_7.repaint()
        self.ui.pushButton_2.setEnabled(self.pagina_actual > 1)
        self.ui.pushButton.setEnabled(self.pagina_actual < self.total_paginas)

    def pagina_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.mostrar_cajas()

    def pagina_siguiente(self):
        self.total_cajas = Caja.contar_cajas()
        self.total_paginas = (self.total_cajas // self.filas_por_pagina) + (1 if self.total_cajas % self.filas_por_pagina else 0)

        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.mostrar_cajas()
    
    def primer_pagina(self):
        if self.pagina_actual != 1:
            self.pagina_actual = 1
            self.mostrar_cajas()

    def ultima_pagina(self):
        if self.pagina_actual != self.total_paginas:
            self.pagina_actual = self.total_paginas
            self.mostrar_cajas()
