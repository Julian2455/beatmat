from PyQt6.QtWidgets import QTableWidgetItem
from models import *  

class ExtintorController:
    def __init__(self, ui):
        self.ui = ui
        self.pagina_actual = 1 
        self.filas_por_pagina = 10  
        self.total_extintores = Extintor.contar_extintores()
        self.total_paginas = (self.total_extintores // self.filas_por_pagina) + (1 if self.total_extintores % self.filas_por_pagina else 0)
        self.mostrar_extintores()
        self.ui.pushButton_2.clicked.connect(self.pagina_anterior) 
        self.ui.pushButton.clicked.connect(self.pagina_siguiente) 
        self.ui.pushButton_3.clicked.connect(self.primer_pagina) 
        self.ui.pushButton_4.clicked.connect(self.ultima_pagina) 
        self.ui.tableWidget.verticalHeader().setVisible(False)

    def mostrar_extintores(self):
        extintores = Extintor.show_all(page=self.pagina_actual, per_page=self.filas_por_pagina)
        self.ui.tableWidget.setRowCount(len(extintores))
        for index, extintor in enumerate(extintores):
            self.ui.tableWidget.setItem(index, 0, QTableWidgetItem(str(extintor.numeracion)))
            self.ui.tableWidget.setItem(index, 1, QTableWidgetItem(extintor.marca))
            self.ui.tableWidget.setItem(index, 2, QTableWidgetItem(extintor.ubicacion))
            self.ui.tableWidget.setItem(index, 3, QTableWidgetItem(extintor.tipo))
            self.ui.tableWidget.setItem(index, 4, QTableWidgetItem(extintor.capacidad))

        self.actualizar_estado_paginado()
    
    def actualizar_estado_paginado(self):
        self.total_extintores = Extintor.contar_extintores()
        self.total_paginas = (self.total_extintores // self.filas_por_pagina) + (1 if self.total_extintores % self.filas_por_pagina else 0)
        self.ui.label_7.setText(f"Página {self.pagina_actual} de {self.total_paginas}")
        self.ui.label_7.repaint()
        self.ui.pushButton_2.setEnabled(self.pagina_actual > 1)
        self.ui.pushButton.setEnabled(self.pagina_actual < self.total_paginas)

    def pagina_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.mostrar_extintores()

    def pagina_siguiente(self):
        self.total_extintores = Extintor.contar_extintores()
        self.total_paginas = (self.total_extintores // self.filas_por_pagina) + (1 if self.total_extintores % self.filas_por_pagina else 0)

        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.mostrar_extintores()
    
    def primer_pagina(self):
        if self.pagina_actual != 1:
            self.pagina_actual = 1
            self.mostrar_extintores()

    def ultima_pagina(self):
        if self.pagina_actual != self.total_paginas:
            self.pagina_actual = self.total_paginas
            self.mostrar_extintores()