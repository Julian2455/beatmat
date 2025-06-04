from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QMenu, QMessageBox, QCheckBox, QLineEdit
from models import *
from utils import get_image
from PyQt6.QtGui import QIcon, QAction, QDoubleValidator, QBrush, QColor, QPainter
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QDate, Qt, QObject, QLocale
from PyQt6.QtCharts import QChartView, QChart, QBarSeries, QBarSet, QCategoryAxis, QValueAxis

class ReportesController(QObject):
    def __init__(self,ui):
        super().__init__()
        self.ui = ui
        self.ui.spinBoxAño.setValue(QDate.currentDate().year())
        self.ui.btnCargarGrafico.clicked.connect(self.graficar_estadisticas)
        self.ui.tableClientesDeben.verticalHeader().setVisible(False)
        self.ui.tableClientesFavor.verticalHeader().setVisible(False)
        self.ui.tableClientesDeben.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.tableClientesFavor.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.chart_view = None
        self.ui.labelGraficoPlaceholder.show()
        self.cargar_datos()

    def cargar_datos(self):
        self.estadisticas()
        self.deudas()
        self.a_favor()

    def estadisticas(self):
        datos=Caja.estado_financiero()
        self.ui.labelTotalVentasValor.setText(str(datos['totales']['total_ventas']))
        self.ui.labelTotalCobrosValor.setText(str(datos['totales']['total_cobros']))
        self.ui.labelTotalAdeudadoValor.setText(str(datos['totales']['total_adeudado']))
        self.ui.labelClientesActivosValor.setText(str(datos['totales']['clientes_activos']))
        self.ui.labelClientesDebenValor.setText(str(datos['estados']['clientes_deben']))
        self.ui.labelClientesFavorValor.setText(str(datos['estados']['clientes_favor']))
        self.ui.labelClientesAlDiaValor.setText(str(datos['estados']['clientes_al_dia']))
    
    def deudas(self):
        clientes=Caja.clientes_con_deuda()
        if clientes:
            self.ui.tableClientesDeben.setRowCount(len(clientes))
            for index, cliente in enumerate(clientes):
                nombre_item = QTableWidgetItem(str(cliente.nombre))
                deuda_item = QTableWidgetItem(str(cliente.deuda))
                deuda_item.setForeground(QBrush(QColor("red")))
                self.ui.tableClientesDeben.setItem(index, 0, nombre_item)
                self.ui.tableClientesDeben.setItem(index, 1, deuda_item)

    def a_favor(self):
        clientes=Caja.clientes_saldo_favor()
        if clientes:
            self.ui.tableClientesFavor.setRowCount(len(clientes))
            for index, cliente in enumerate(clientes):
                nombre_item = QTableWidgetItem(str(cliente.nombre))
                saldo_favor_item = QTableWidgetItem(str(cliente.saldo_favor))
                saldo_favor_item.setForeground(QBrush(QColor("green")))
                self.ui.tableClientesFavor.setItem(index, 0, nombre_item)   
                self.ui.tableClientesFavor.setItem(index, 1, saldo_favor_item)  
    
    def graficar_estadisticas(self):
        año=self.ui.spinBoxAño.value()
        datos_grafico=Caja.obtener_datos_grafico_mensual(año)
        self.ui.labelGraficoPlaceholder.hide()
        if self.chart_view is not None:
            self.ui.verticalLayout_frame_grafico.removeWidget(self.chart_view)
            self.chart_view.deleteLater()
            self.chart_view = None 
        set_ventas = QBarSet("Ventas")
        set_cobros = QBarSet("Cobros")
        set_adeudado = QBarSet("Adeudado")
        categories = []
        for dato in datos_grafico:
            set_ventas.append(dato['ventas'])
            set_cobros.append(dato['cobros'])
            set_adeudado.append(dato['adeudado'])
            categories.append(dato['mes'])
        series = QBarSeries()
        series.append(set_ventas)
        series.append(set_cobros)
        series.append(set_adeudado)
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(f"Estadísticas Mensuales del Año {año}")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        axis_x = QCategoryAxis()
        for i, category in enumerate(categories):
            axis_x.append(category, i) 
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)
        axis_y = QValueAxis()
        max_value = 0
        for dato in datos_grafico:
            max_value = max(max_value, dato['ventas'], dato['cobros'], dato['adeudado'])
        axis_y.setRange(0, max_value * 1.1 if max_value > 0 else 10) 
        axis_y.setLabelFormat("%d")
        axis_y.setTitleText("Monto")
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.ui.verticalLayout_frame_grafico.addWidget(self.chart_view)