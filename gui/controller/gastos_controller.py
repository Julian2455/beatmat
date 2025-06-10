from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt, QObject, QDate
from PyQt6.QtGui import QAction, QColor, QPixmap, QIcon, QPainter
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from PyQt6 import QtCore, QtWidgets
from models import *  
from utils import get_image
from datetime import timedelta

class GastosController(QObject):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.query=None
        self.pagina_actual = 1
        self.filas_por_pagina = 10
        self.fecha_filtro_activo = False
        self.total_gastos = Gastos.contar_gastos()
        self.total_paginas = (self.total_gastos // self.filas_por_pagina) + (1 if self.total_gastos % self.filas_por_pagina else 0)
        self.mostrar_gastos()
        self.ui.btnPreviousPage.clicked.connect(self.pagina_anterior) 
        self.ui.btnNextPage.clicked.connect(self.pagina_siguiente) 
        self.ui.btnFirstPage.clicked.connect(self.primer_pagina) 
        self.ui.btnLastPage.clicked.connect(self.ultima_pagina) 
        self.ui.btnRestaurar.setVisible(False)
        self.ui.tableGastos.verticalHeader().setVisible(False)
        self.ui.tableGastos.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.ui.btnRestaurar.clicked.connect(self.limpiar_filtros) 
        self.ui.btnNextPage.setIcon(QIcon(get_image("sssiguiente"))) 
        self.ui.btnPreviousPage.setIcon(QIcon(get_image("anterior"))) 
        self.ui.btnFirstPage.setIcon(QIcon(get_image("anterior_1"))) 
        self.ui.btnLastPage.setIcon(QIcon(get_image("proximo_1"))) 
        self.ui.pushButton.setIcon(QIcon(get_image("dinero"))) 
        self.setupDateEdits()
        self.meses_combobox()
        self.ui.btnGenerarGrafico.clicked.connect(self.mostrar_grafico) 

    def setupDateEdits(self):
        fecha_minima_bd = Gastos.obtener_fecha_minima()
        fecha_minima = QDate.fromString((fecha_minima_bd - timedelta(days=1)).strftime("%Y-%m-%d"), "yyyy-MM-dd")
        self.ui.dateEdit.setMinimumDate(fecha_minima)
        self.ui.dateEdit.setSpecialValueText("--/--/--")
        self.ui.dateEdit.setDate(fecha_minima)
        self.fecha_filtro_activo = False
        self.ui.dateEdit.dateChanged.connect(self.on_date_changed)

    def on_date_changed(self, date):
        if date == self.ui.dateEdit.minimumDate():
            self.fecha_filtro_activo = False
            self.mostrar_gastos()
            return
        self.fecha_filtro_activo = True
        self.ui.btnRestaurar.setVisible(True)
        self.fecha_py = date.toPyDate()
        self.pagina_actual = 1 
        self.mostrar_gastos()
    
    def limpiar_filtros(self):
        self.ui.dateEdit.setDate(self.ui.dateEdit.minimumDate())
        self.fecha_filtro_activo = False
        self.fecha_py = None
        self.ui.btnRestaurar.setVisible(False)
        self.pagina_actual = 1
        self.mostrar_gastos()

    def mostrar_gastos(self):
        if self.fecha_filtro_activo:
            resultados = Gastos.buscar(self.fecha_py, page=self.pagina_actual, per_page=self.filas_por_pagina)
        else:
            resultados = Gastos.show_all(page=self.pagina_actual, per_page=self.filas_por_pagina)
        self.ui.tableGastos.setRowCount(len(resultados))
        for index, resultado in enumerate(resultados):
            gasto = resultado
            id_gasto = QTableWidgetItem(str(gasto.id))
            id_gasto.setData(Qt.ItemDataRole.UserRole, gasto.id)
            self.ui.tableGastos.setItem(index, 0, QTableWidgetItem(str(gasto.fecha.strftime("%d-%m-%Y"))))
            gasto_formateado = f"{int(gasto.gasto):,}".replace(",", ".")
            self.ui.tableGastos.setItem(index, 1, QTableWidgetItem(gasto_formateado))
            self.ui.tableGastos.setItem(index, 2, QTableWidgetItem(str(gasto.categoria_nombre)))
            self.ui.tableGastos.setItem(index, 3, QTableWidgetItem(str(gasto.insumo)))
        self.actualizar_estado_paginado()

    def actualizar_estado_paginado(self):
        if self.fecha_filtro_activo:
            self.total_gastos = Gastos.contar_buscar(self.fecha_py)
        else:
            self.total_gastos = Gastos.contar_gastos()
        self.total_paginas = max(1, (self.total_gastos // self.filas_por_pagina) + (1 if self.total_gastos % self.filas_por_pagina else 0))
        if self.pagina_actual > self.total_paginas:
            self.pagina_actual = max(1, self.total_paginas)
        self.ui.labelPageInfo.setText(f"Página {self.pagina_actual} de {self.total_paginas}")
        self.ui.labelPageInfo.repaint()
        self.ui.btnPreviousPage.setEnabled(self.pagina_actual > 1)
        self.ui.btnNextPage.setEnabled(self.pagina_actual < self.total_paginas)

    def pagina_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.mostrar_gastos()

    def pagina_siguiente(self):
        self.total_gastos = Gastos.contar_gastos()
        self.total_paginas = (self.total_gastos // self.filas_por_pagina) + (1 if self.total_gastos % self.filas_por_pagina else 0)

        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.mostrar_gastos()
    
    def primer_pagina(self):
        if self.pagina_actual != 1:
            self.pagina_actual = 1
            self.mostrar_gastos()

    def ultima_pagina(self):
        if self.pagina_actual != self.total_paginas:
            self.pagina_actual = self.total_paginas
            self.mostrar_gastos()

    def meses_combobox(self):
        self.ui.comboBoxMes.clear()
        self.ui.comboBoxMes.addItem("Todos")
        meses=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        num=1
        for mes in meses:
            self.ui.comboBoxMes.addItem(mes)
            index=self.ui.comboBoxMes.count()-1
            self.ui.comboBoxMes.setItemData(index, num, QtCore.Qt.ItemDataRole.UserRole)
            num+=1
    
    def mostrar_grafico(self):
        año = self.ui.spinBoxAño.value()
        mes_seleccionado = self.ui.comboBoxMes.currentData(QtCore.Qt.ItemDataRole.UserRole)
        mes_para_db = mes_seleccionado if mes_seleccionado is not None else None
        datos_grafico = Gastos.gastos_por_categoria_mes(año, mes_para_db)
        if hasattr(self, 'chart_view') and self.chart_view is not None:
            self.ui.layoutGrafico.removeWidget(self.chart_view) 
            self.chart_view.deleteLater()
            self.chart_view = None
        self.ui.labelPlaceholder.hide() 
        if not datos_grafico:
            self.ui.labelPlaceholder.setText("No hay datos de gastos para el período seleccionado.")
            self.ui.labelPlaceholder.show()
            self.ui.labelEstadisticas.setText("Total de gastos del período: $0.00")
            self.ui.labelEstadisticas.hide() 
            return
        series = QPieSeries()
        total_gastos_mes = sum(item['total_gasto'] for item in datos_grafico)
        for dato in datos_grafico:
            categoria = dato['categoria']
            total_gasto = dato['total_gasto']
            slice = QPieSlice(categoria, total_gasto)
            if total_gastos_mes > 0:
                percentage = (total_gasto / total_gastos_mes) * 100
                slice.setLabel(f"{categoria}: ${total_gasto:,.0f} ({percentage:.1f}%)".replace(",", "."))
            else:
                slice.setLabel(f"{categoria}: ${total_gasto:,.0f}".replace(",", "."))
            series.append(slice)
        chart = QChart()
        chart.addSeries(series)
        if mes_seleccionado is None: 
            chart.setTitle(f"Gastos por Categoría - Año {año}")
        else:
            mes_nombre = self.ui.comboBoxMes.currentText()
            chart.setTitle(f"Gastos por Categoría - {mes_nombre} {año}")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.ui.layoutGrafico.addWidget(self.chart_view)
        self.ui.labelEstadisticas.setText(f"Total de gastos del período: ${total_gastos_mes:,.0f}".replace(",", "."))
        self.ui.labelEstadisticas.show()