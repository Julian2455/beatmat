from PyQt6.QtWidgets import QTableWidgetItem, QPushButton, QMessageBox, QMenu, QFileDialog
from PyQt6.QtGui import QAction, QColor, QPixmap, QIcon, QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtPrintSupport import QPrinter
from models import *
from utils import get_image
from datetime import datetime, timedelta
import os, tempfile, platform, webbrowser
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer, Indenter, Paragraph   
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class ClientController:
    def __init__(self, ui):
        self.ui = ui
        self.query=None
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
        self.ui.tableWidget.doubleClicked.connect(self.extintores_clientes)
        self.ui.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.tableWidget.customContextMenuRequested.connect(self.mostrar_menu_contextual)
        self.edit_form_cli = None
        self.ui.lineEdit.textChanged.connect(self.buscar_cliente)
        self.ui.label.setPixmap(QPixmap(get_image("buscar")))
        self.ui.pushButton.setIcon(QIcon(get_image("sssiguiente"))) 
        self.ui.pushButton_2.setIcon(QIcon(get_image("anterior"))) 
        self.ui.pushButton_3.setIcon(QIcon(get_image("anterior_1"))) 
        self.ui.pushButton_4.setIcon(QIcon(get_image("proximo_1"))) 
        self.ui.pushButton_5.setIcon(QIcon(get_image("agregar-usuario2")))

    def mostrar_clientes(self):
        if self.query:
            clientes=Cliente.buscar(self.query,page=self.pagina_actual, per_page=self.filas_por_pagina)
        else:
            clientes = Cliente.show_all(page=self.pagina_actual, per_page=self.filas_por_pagina)
        self.ui.tableWidget.setRowCount(len(clientes))
        for index, cliente in enumerate(clientes):
            id_cliente = QTableWidgetItem(cliente.nombre)
            id_cliente.setData(Qt.ItemDataRole.UserRole, cliente.id)
            self.ui.tableWidget.setItem(index, 0, id_cliente)
            self.ui.tableWidget.setItem(index, 1, QTableWidgetItem(cliente.direccion))
            self.ui.tableWidget.setItem(index, 2, QTableWidgetItem(str(cliente.telefono)))

        self.actualizar_estado_paginado()

    def mostrar_menu_contextual(self, pos):
        index = self.ui.tableWidget.indexAt(pos)
        if not index.isValid():
            return
        menu = QMenu(self.ui.tableWidget)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #CCCCCC;
            }
            QMenu::item {
                padding: 5px 15px;
                background-color: white;
            }
            QMenu::item:selected {
                background-color: #E0E0E0;
                color: black;
            }
        """)
        editar_action = QAction("Editar", self.ui.tableWidget)
        eliminar_action = QAction("Eliminar", self.ui.tableWidget)
        editar_action.triggered.connect(self.editar_cliente)
        eliminar_action.triggered.connect(self.eliminar_cliente)
        menu.addAction(editar_action)
        menu.addAction(eliminar_action)
        menu.exec(self.ui.tableWidget.viewport().mapToGlobal(pos))
    
    def set_edit_form_cli(self, edit_form_cli):
        self.edit_form_cli = edit_form_cli
    
    def obtener_id_cliente(self):
        item_seleccionado = self.ui.tableWidget.currentItem()
        if item_seleccionado:
            fila = item_seleccionado.row()
            item_con_id = self.ui.tableWidget.item(fila, 0) 
            id_cliente = item_con_id.data(Qt.ItemDataRole.UserRole)
            return id_cliente
        return None

    def editar_cliente(self):
        id_cliente = self.obtener_id_cliente()
        if id_cliente and self.edit_form_cli:
            self.edit_form_cli.setWindowTitle("Editar Cliente")
            cliente = Cliente.get_by_id(id_cliente)
            if cliente:
                self.edit_form_cli.label_2.setText("EDITAR CLIENTE")
                self.edit_form_cli.lineEdit.setText(cliente.nombre)
                self.edit_form_cli.lineEdit_2.setText(cliente.direccion)
                self.edit_form_cli.lineEdit_3.setText(str(cliente.telefono))
                self.edit_client_controller.cliente_id = id_cliente
                self.edit_form_cli.mostrar_form()
    
    def eliminar_cliente(self):
        id_cliente = self.obtener_id_cliente()
        if id_cliente: #Aca tiene que ir la logica para eliminar y el mensaje, pero hay que hacerlo despues, por la relacion con las otras tablas
            print(f"Eliminar : {id_cliente}")

    def actualizar_estado_paginado(self):
        if self.query:
            self.total_clientes=Cliente.contar_buscar(self.query)
        else:
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

    def extintores_clientes(self,index):
        nombre = self.ui.tableWidget.item(index.row(), 0).text()
        domicilio = self.ui.tableWidget.item(index.row(), 1).text()
        telefono = self.ui.tableWidget.item(index.row(), 2).text()
        self.asociacion_ui.labelCliente.setText(f'Extintores asociados a {nombre}')
        id_cliente=self.obtener_id_cliente()
        self.ui.hide()
        self.asociacion_ui.show()
        self.asociacion_ui.pushButton.setIcon(QIcon(get_image("print")))
        self.asociacion_ui.tableWidgetExtintores.verticalHeader().setVisible(False)
        self.asociacion_ui.tableWidgetExtintores.setRowCount(0)
        self.asociacion_ui.pushButton.clicked.connect(lambda: self.imprimir_extintores_cliente(nombre,domicilio,telefono))
        extintores=Extintor.extintor_asociado_cliente(id_cliente)
        if extintores:
            self.asociacion_ui.tableWidgetExtintores.setRowCount(len(extintores))
            for index, resultado in enumerate(extintores):
                self.asociacion_ui.tableWidgetExtintores.setItem(index, 0, QTableWidgetItem(str(resultado["numeracion"])))
                self.asociacion_ui.tableWidgetExtintores.setItem(index, 1, QTableWidgetItem(str(resultado["marca"])))
                self.asociacion_ui.tableWidgetExtintores.setItem(index, 2, QTableWidgetItem(str(resultado["tipo"])))
                self.asociacion_ui.tableWidgetExtintores.setItem(index, 3, QTableWidgetItem(str(resultado["capacidad"])))
                recarga = resultado["ultima_recarga"]
                if recarga:
                    self.asociacion_ui.tableWidgetExtintores.setItem(index, 4, QTableWidgetItem(str(recarga.vto_control_recarga_formateado)))
                    self.asociacion_ui.tableWidgetExtintores.setItem(index, 5, QTableWidgetItem(str(recarga.nuevo_control_recarga_formateado)))
                    self.asociacion_ui.tableWidgetExtintores.setItem(index, 6, QTableWidgetItem(str(recarga.vto_ph)))
                tarea = resultado["ultima_tarea"]
                if tarea:
                    valores = [
                        tarea.tamizacion,
                        tarea.peso,
                        tarea.control_tacho,
                        tarea.relleno_polvo,
                        tarea.cambio_manometro,
                        tarea.oring,
                        tarea.gatillo,
                        tarea.pintura,
                        tarea.interior,
                        tarea.valvula,
                        tarea.bastago_bronce,
                    ]
                    for i, valor in enumerate(valores):
                        item = QTableWidgetItem("")
                        if isinstance(valor, bool):
                            item.setText("SI" if valor else "NO")
                        else:
                            item.setText(str(valor))

                        self.asociacion_ui.tableWidgetExtintores.setItem(index, 7 + i, item)
                    observacion = tarea.observacion
                    if not observacion or observacion == "Null":
                        observacion = "-"
                    self.asociacion_ui.tableWidgetExtintores.setItem(index, 18, QTableWidgetItem(observacion))
                    self.asociacion_ui.tableWidgetExtintores.setItem(index, 19, QTableWidgetItem(str(resultado["ubicacion"])))
                self.asociacion_ui.tableWidgetExtintores.resizeColumnsToContents()

    def buscar_cliente(self):
        previous_query = self.query
        self.query = self.ui.lineEdit.text()
        if previous_query != self.query:
            self.pagina_actual = 1
        self.mostrar_clientes()


    def imprimir_extintores_cliente(self, nombre, domicilio, telefono):
        temp_dir = tempfile.gettempdir()
        archivo_pdf = os.path.join(temp_dir, f"reporte_extintores_{nombre}.pdf")
        pdf = SimpleDocTemplate(
            archivo_pdf,
            pagesize=A4,
            leftMargin=2,
            rightMargin=-2,
            topMargin=-6,
            bottomMargin=0
        )
        elementos = []
        ruta_imagen = get_image("encabezado-impresion")
        if os.path.exists(ruta_imagen):
            imagen_encabezado = Image(ruta_imagen, height=130)
            imagen_encabezado.hAlign = 'CENTER'
            elementos.append(imagen_encabezado)
        else:
            print("⚠️ Imagen no encontrada:", ruta_imagen)
        estilo_titulo = ParagraphStyle(
            name="TituloTabla",
            fontSize=12,
            leading=14,
            alignment=0,  
            spaceAfter=6,
            fontName="Helvetica-Bold",
            textColor=colors.red
        )
        titulo_cliente=Paragraph("DATOS DEL CLIENTE", estilo_titulo)
        data_cliente = [
            ["Nombre", "Domicilio", "Telefono"],
            [nombre, domicilio, telefono]
        ]
        tabla_cliente = Table(data_cliente, colWidths=[150]*3,hAlign='LEFT' )
        tabla_cliente.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#d0d0d0")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (0, 0),"LEFT"),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        elementos.append(Indenter(left=30))
        elementos.append(Spacer(10, 30))
        elementos.append(titulo_cliente)
        elementos.append(tabla_cliente)
        elementos.append(Spacer(10, 45))
        tabla = self.asociacion_ui.tableWidgetExtintores
        filas = tabla.rowCount()
        columnas = tabla.columnCount()
        encabezados = [tabla.horizontalHeaderItem(col).text() if tabla.horizontalHeaderItem(col) else f"Col {col+1}" for col in range(columnas)]
        data_total = []
        for row in range(filas):
            fila = []
            for col in range(columnas):
                item = tabla.item(row, col)
                fila.append(item.text() if item else "")
            data_total.append(fila)
        indices_1 = list(range(0, 7))
        data1 = [[encabezados[i] for i in indices_1]] + [[fila[i] for i in indices_1] for fila in data_total]
        titulo_extintor=Paragraph("DATOS DEL EXTINTOR", estilo_titulo)
        tabla1 = Table(data1, repeatRows=1, hAlign='LEFT')
        tabla1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e0e0e0")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1),"CENTER"),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        elementos.append(titulo_extintor)
        elementos.append(tabla1)
        elementos.append(Spacer(10, 40))
        indices_2 = [0] + list(range(7, min(20, columnas)))
        data2 = [[encabezados[i] for i in indices_2]] + [[fila[i] for i in indices_2] for fila in data_total]
        titulo_servicio=Paragraph("DETALLES DEL SERVICIO", estilo_titulo)
        tabla2 = Table(data2, repeatRows=1, hAlign='LEFT')
        tabla2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e0e0e0")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), "CENTER"),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        elementos.append(titulo_servicio)
        elementos.append(tabla2)
        pdf.build(elementos)
        webbrowser.open(f'file://{archivo_pdf}')
