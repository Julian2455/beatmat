from PyQt6.QtWidgets import QTableWidgetItem, QPushButton, QMessageBox
from PyQt6.QtGui import QIcon
from models import *  
from db import SessionLocal

class ClientController:
    def __init__(self, ui, main_window):
        self.ui = ui
        self.main_window = main_window
        self.pagina_actual = 1 
        self.filas_por_pagina = 10  
        self.total_clientes = Cliente.contar_clientes()
        self.total_paginas = (self.total_clientes // self.filas_por_pagina) + (1 if self.total_clientes % self.filas_por_pagina else 0)
        self.mostrar_clientes()
        self.ui.pushButton_2.clicked.connect(self.pagina_anterior) 
        self.ui.pushButton.clicked.connect(self.pagina_siguiente) 
        self.ui.pushButton_3.clicked.connect(self.primer_pagina) 
        self.ui.pushButton_4.clicked.connect(self.ultima_pagina) 
        self.ui.tableWidget.verticalHeader().setVisible(False)


    def mostrar_clientes(self):
        clientes = Cliente.show_all(page=self.pagina_actual, per_page=self.filas_por_pagina)
        self.ui.tableWidget.setRowCount(len(clientes))
        for index, cliente in enumerate(clientes):
            cliente_id = cliente.id
            nombrec = cliente.nombre
            direccionc = cliente.direccion
            btn_edit = QPushButton("")
            btn_edit.setIcon(QIcon("resources/images/boligrafo"))
            btn_delete = QPushButton("")
            btn_delete.setIcon(QIcon("resources/images/basura"))
            btn_edit.clicked.connect(lambda _, cid=cliente_id, nom=nombrec, dire=direccionc : self.obtener_datos_cliente("editar", cid,nom,dire))
            btn_delete.clicked.connect(lambda _, cid=cliente_id, nom=nombrec, dire=direccionc : self.obtener_datos_cliente("eliminar", cid,nom,dire))
            self.ui.tableWidget.setCellWidget(index, 0, btn_delete)
            self.ui.tableWidget.setCellWidget(index, 1, btn_edit)
            self.ui.tableWidget.setItem(index, 2, QTableWidgetItem(cliente.nombre))  
            self.ui.tableWidget.setItem(index, 3, QTableWidgetItem(cliente.direccion))

            self.ui.tableWidget.resizeColumnToContents(0)
            self.ui.tableWidget.resizeColumnToContents(1)

        self.actualizar_estado_paginado()
    
    def obtener_datos_cliente(self,accion, cliente_id, nombrec, direccionc):
        cliente = [cliente_id, nombrec, direccionc]
        if accion == "editar":
            self.main_window.client_form_controller.abrir_form_edit(cliente)
        elif accion == "eliminar":
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Confirmar eliminación")
            msg.setText(f"¿Estás seguro que deseas eliminar al usuario <b>'{nombrec}'</b>?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg.setDefaultButton(QMessageBox.StandardButton.No)
            respuesta=msg.exec()
            self.main_window.client_form_controller.confirmar_eliminacion(respuesta,cliente_id)

    def actualizar_estado_paginado(self):
        self.total_clientes = Cliente.contar_clientes()
        self.total_paginas = (self.total_clientes // self.filas_por_pagina) + (1 if self.total_clientes % self.filas_por_pagina else 0)
        self.ui.label_7.setText(f"Página {self.pagina_actual} de {self.total_paginas}")
        self.ui.label_7.repaint()
        self.ui.pushButton_2.setEnabled(self.pagina_actual > 1)
        self.ui.pushButton.setEnabled(self.pagina_actual < self.total_paginas)

    def pagina_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.mostrar_clientes()

    def pagina_siguiente(self):
        self.total_clientes = Cliente.contar_clientes()
        self.total_paginas = (self.total_clientes // self.filas_por_pagina) + (1 if self.total_clientes % self.filas_por_pagina else 0)

        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.mostrar_clientes()
    
    def primer_pagina(self):
        if self.pagina_actual != 1:
            self.pagina_actual = 1
            self.mostrar_clientes()

    def ultima_pagina(self):
        if self.pagina_actual != self.total_paginas:
            self.pagina_actual = self.total_paginas
            self.mostrar_clientes()

