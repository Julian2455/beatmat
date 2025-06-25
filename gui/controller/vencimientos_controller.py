from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt6.QtGui import QIcon, QIntValidator, QColor, QFont, QPixmap
from PyQt6.QtCore import QDate
from models import *
from utils import get_image
from datetime import datetime, timedelta
import os, tempfile, webbrowser
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer, LongTable, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class VencimientosController:
    def __init__(self, ui):
        self.ui = ui
        self.dias_vencimiento=None
        self.pagina_actual = 1
        self.filas_por_pagina = 10
        self.total_vencimientos = Extintor.contar_vencimientos_proximos()
        self.total_paginas = (self.total_vencimientos // self.filas_por_pagina) + (1 if self.total_vencimientos % self.filas_por_pagina else 0)
        self.mostrar_vencimientos()
        self.ui.pushButton_2.clicked.connect(self.pagina_anterior) 
        self.ui.pushButton.clicked.connect(self.pagina_siguiente) 
        self.ui.pushButton_3.clicked.connect(self.primer_pagina) 
        self.ui.pushButton_4.clicked.connect(self.ultima_pagina) 
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.pushButton.setIcon(QIcon(get_image("sssiguiente"))) 
        self.ui.pushButton_2.setIcon(QIcon(get_image("anterior"))) 
        self.ui.pushButton_3.setIcon(QIcon(get_image("anterior_1"))) 
        self.ui.pushButton_4.setIcon(QIcon(get_image("proximo_1"))) 
        self.ui.imprimir.setIcon(QIcon(get_image("print")))
        self.ui.label_3.setPixmap(QPixmap(get_image("calendariod")))
        self.ui.restaurar.clicked.connect(self.restaurar_cuenta)
        self.ui.pushButton_5.clicked.connect(self.calcular_vencimientos_dias)
        self.ui.imprimir.clicked.connect(self.imprimir_vencimientos_btn)
        self.ui.lineEdit.setValidator(QIntValidator(1,9999))

    def mostrar_vencimientos(self):
        mostrar_fecha_actual = datetime.today().date()
        fecha_actual_formateada = mostrar_fecha_actual.strftime("%d-%m-%Y")
        dias = self.dias_vencimiento or 30  
        ids = Extintor.vencimientos_proximos(dias, page=self.pagina_actual, per_page=self.filas_por_pagina)
        vencimientos_proximos=Extintor.detalles_vencimientos_por_ids(ids)
        self.ui.dateEdit.setText(str(fecha_actual_formateada))
        self.ui.text_dias.setText(f"⚠️¡Los extintores mostrados en pantalla se vencen dentro de {dias} días!")
        self.ui.tableWidget.setRowCount(0)
        if vencimientos_proximos:
            self.ui.tableWidget.setRowCount(len(vencimientos_proximos))
            for index, venc in enumerate(vencimientos_proximos):
                self.ui.tableWidget.setItem(index, 0, QTableWidgetItem(str(venc.cliente)))
                self.ui.tableWidget.setItem(index, 1, QTableWidgetItem(str(venc.ubicacion)))
                self.ui.tableWidget.setItem(index, 2, QTableWidgetItem(str(venc.numeracion)))
                self.ui.tableWidget.setItem(index, 3, QTableWidgetItem(str(venc.marca)))
                fecha_recarga = venc.vto_recarga.strftime("%d-%m-%Y") if venc.vto_recarga else ""
                self.ui.tableWidget.setItem(index, 4, QTableWidgetItem(fecha_recarga))
                self.ui.tableWidget.setItem(index, 5, QTableWidgetItem(str(venc.vto_ph)))
                fecha_actual = datetime.today().date()
                dias_restantes = (venc.vto_recarga - fecha_actual).days
                item_estado = QTableWidgetItem()
                if dias_restantes < 0:
                    item_estado.setText("VENCIDO")
                    item_estado.setForeground(QColor("red"))
                elif dias_restantes < 10:
                    item_estado.setText(f"{dias_restantes} días")
                    item_estado.setForeground(QColor("red"))
                elif 10 <= dias_restantes < 20:
                    item_estado.setText(f"{dias_restantes} días")
                    item_estado.setForeground(QColor("orange"))
                else:
                    item_estado.setText(f"{dias_restantes} días")
                    item_estado.setForeground(QColor("green"))
                font = QFont()
                font.setBold(True)
                item_estado.setFont(font)
                self.ui.tableWidget.setItem(index, 6, item_estado)
            self.ui.tableWidget.resizeColumnToContents(4)
            self.ui.tableWidget.resizeColumnToContents(5)
            self.ui.tableWidget.resizeColumnToContents(6)
            self.actualizar_estado_paginado()
            self.mostrar_btn_restaurar()
            print(f"[DEBUG] Mostrando vencimientos para {dias} días - Página {self.pagina_actual}")


    def calcular_vencimientos_dias(self):
        texto = self.ui.lineEdit.text()
        if texto.strip() == "":
            dias = 30
            self.ui.lineEdit.clear()
        else:
            try:
                dias = int(texto)
            except ValueError:
                dias = 30
                self.ui.lineEdit.clear()

        self.dias_vencimiento = dias
        self.pagina_actual = 1
        self.mostrar_vencimientos()


    def actualizar_estado_paginado(self):
        dias = self.dias_vencimiento or 30
        self.total_vencimientos = Extintor.contar_vencimientos_proximos(dias)
        self.total_paginas = (self.total_vencimientos // self.filas_por_pagina) + (1 if self.total_vencimientos % self.filas_por_pagina else 0)
        self.ui.label_7.setText(f"Página {self.pagina_actual} de {self.total_paginas}")
        self.ui.label_7.repaint()
        self.ui.pushButton_2.setEnabled(self.pagina_actual > 1)
        self.ui.pushButton.setEnabled(self.pagina_actual < self.total_paginas)

    def pagina_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.mostrar_vencimientos()

    def pagina_siguiente(self):
        dias = self.dias_vencimiento or 30
        self.total_vencimientos = Extintor.contar_vencimientos_proximos(dias)
        self.total_paginas = (self.total_vencimientos // self.filas_por_pagina) + (1 if self.total_vencimientos % self.filas_por_pagina else 0)

        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.mostrar_vencimientos()
    
    def primer_pagina(self):
        if self.pagina_actual != 1:
            self.pagina_actual = 1
            self.mostrar_vencimientos()

    def ultima_pagina(self):
        if self.pagina_actual != self.total_paginas:
            self.pagina_actual = self.total_paginas
            self.mostrar_vencimientos()

    def mostrar_btn_restaurar(self):
        calculadora_activa = (
            self.ui.lineEdit.text() != ""
        )
        self.ui.restaurar.setVisible(calculadora_activa)
    
    def restaurar_cuenta(self):
        self.dias_vencimiento=None
        self.ui.lineEdit.clear()
        self.pagina_actual = 1
        self.mostrar_vencimientos()
        self.ui.restaurar.setVisible(False)
    
    def imprimir_vencimientos_btn(self):
        dias = self.dias_vencimiento or 30
        self.imprimir_vencimientos(dias)


    def imprimir_vencimientos(self, dias):
        temp_dir = tempfile.gettempdir()
        archivo_pdf = os.path.join(temp_dir, f"Vencimientos_Extintores.pdf")
        pdf = SimpleDocTemplate(
            archivo_pdf,
            pagesize=landscape(A4),
            leftMargin=2,
            rightMargin=-2,
            topMargin=-6,
            bottomMargin=0
        )
        elementos = []
        estilo_titulo = ParagraphStyle(
            name="TituloTabla",
            fontSize=12,
            leading=14,
            alignment=0,  
            spaceAfter=6,
            fontName="Helvetica-Bold",
            textColor=colors.black
        )
        dias = dias
        ids = Extintor.print_vencimientos(dias)
        vencimientos_proximos=Extintor.detalles_vencimientos_por_ids(ids)
        encabezados = ["Cliente", "Ubicación", "N° Extintor", "Marca", "Vencimiento de recarga", "Vencimiento de prueba hidráulica", "Días restantes"]
        dato = [encabezados]
        fecha_actual = datetime.today().date()
        for venc in vencimientos_proximos:
            dias_restantes = (venc.vto_recarga - fecha_actual).days if venc.vto_recarga else 0
            fila = [
                str(venc.cliente),
                str(venc.ubicacion),
                str(venc.numeracion),
                str(venc.marca),
                str(venc.vto_recarga),
                str(venc.vto_ph),
                dias_restantes
            ]
            dato.append(fila)
        titulo_vencimiento=Paragraph("PLANILLA DE SEGUIMIENTO - VENCIMIENTOS", estilo_titulo)
        elementos.append(Spacer(10, 40))
        vencimientos_proximos = LongTable(dato, repeatRows=1, hAlign='LEFT')
        vencimientos_proximos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e0e0e0")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1),"CENTER"),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        elementos.append(titulo_vencimiento)
        elementos.append(Spacer(10, 40))
        elementos.append(vencimientos_proximos)
        elementos.append(Spacer(10, 40))
        pdf.build(elementos)
        webbrowser.open(f'file://{archivo_pdf}')