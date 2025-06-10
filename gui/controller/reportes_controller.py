from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QMenu, QMessageBox, QCheckBox, QLineEdit
from models import *
from utils import get_image
from PyQt6.QtGui import QIcon, QAction, QDoubleValidator, QBrush, QColor, QPainter
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QDate, Qt, QObject, QLocale
from PyQt6.QtCharts import QChartView, QChart, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis, QPieSeries, QPieSlice

class ReportesController(QObject):
    def __init__(self,ui):
        super().__init__()
        self.ui = ui
        self.locale = QLocale(QLocale.Language.Spanish, QLocale.Country.Argentina)
        self.ui.spinBoxAño.setValue(QDate.currentDate().year())
        self.ui.btnCargarGrafico.clicked.connect(self.graficar_estadisticas)
        self.ui.tableClientesDeben.verticalHeader().setVisible(False)
        self.ui.tableClientesFavor.verticalHeader().setVisible(False)
        self.ui.tableResumenMensual.verticalHeader().setVisible(False)
        self.ui.tableClientesDeben.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.tableClientesFavor.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.tableResumenMensual.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.chart_view = None
        self.ganancias_chart_view = None
        self.ui.labelGraficoGananciasPlaceholder.show()
        self.ui.labelGraficoPlaceholder.show()
        self.ui.btnCargarGanancias.clicked.connect(self.graficar_ganancias)
        self.ui.spinBoxAñoGanancias.setValue(QDate.currentDate().year())
        self.meses_combobox()
        self.cargar_datos()

    def cargar_datos(self):
        self.estadisticas()
        self.deudas()
        self.a_favor()

    def estadisticas(self):
        datos=Caja.estado_financiero()
        self.ui.labelTotalVentasValor.setText(self.locale.toString(float(datos['totales']['total_ventas']), 'f', 2))
        self.ui.labelTotalCobrosValor.setText(self.locale.toString(float(datos['totales']['total_cobros']), 'f', 2))
        self.ui.labelTotalAdeudadoValor.setText(self.locale.toString(float(datos['totales']['total_adeudado']), 'f', 2))
        self.ui.labelClientesActivosValor.setText(self.locale.toString(float(datos['totales']['clientes_activos']), 'f',0))
        self.ui.labelClientesDebenValor.setText(self.locale.toString(float(datos['estados']['clientes_deben']), 'f',0))
        self.ui.labelClientesFavorValor.setText(self.locale.toString(float(datos['estados']['clientes_favor']), 'f',0))
        self.ui.labelClientesAlDiaValor.setText(self.locale.toString(float(datos['estados']['clientes_al_dia']), 'f',0))
    
    def deudas(self):
        clientes=Caja.clientes_con_deuda()
        if clientes:
            self.ui.tableClientesDeben.setRowCount(len(clientes))
            for index, cliente in enumerate(clientes):
                nombre_item = QTableWidgetItem(str(cliente.nombre))
                deuda_item = QTableWidgetItem(self.locale.toString(float(cliente.deuda)))
                deuda_item.setForeground(QBrush(QColor("red")))
                self.ui.tableClientesDeben.setItem(index, 0, nombre_item)
                self.ui.tableClientesDeben.setItem(index, 1, deuda_item)

    def a_favor(self):
        clientes=Caja.clientes_saldo_favor()
        if clientes:
            self.ui.tableClientesFavor.setRowCount(len(clientes))
            for index, cliente in enumerate(clientes):
                nombre_item = QTableWidgetItem(str(cliente.nombre))
                saldo_favor_item = QTableWidgetItem(self.locale.toString(float(cliente.saldo_favor)))
                saldo_favor_item.setForeground(QBrush(QColor("green")))
                self.ui.tableClientesFavor.setItem(index, 0, nombre_item)   
                self.ui.tableClientesFavor.setItem(index, 1, saldo_favor_item)  
    
    def graficar_estadisticas(self):
        año=self.ui.spinBoxAño.value()
        datos_grafico=Caja.obtener_datos_grafico_mensual(año)
        self.cargar_detalles_estadisticas(año)
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
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
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
    
    def cargar_detalles_estadisticas(self,año):
        datos=Caja.obtener_resumen_mensual_detallado(año)
        if datos:
            self.ui.tableResumenMensual.setRowCount(len(datos))
            for index, dato in enumerate(datos):
                self.ui.tableResumenMensual.setItem(index, 0, QTableWidgetItem(dato['mes_nombre']))
                self.ui.tableResumenMensual.setItem(index, 1, QTableWidgetItem(self.locale.toString(float(dato['total_ventas']), 'f', 2)))
                self.ui.tableResumenMensual.setItem(index, 2, QTableWidgetItem(self.locale.toString(float(dato['total_cobros']), 'f', 2)))
                self.ui.tableResumenMensual.setItem(index, 3, QTableWidgetItem(self.locale.toString(float(dato['total_adeudado']), 'f', 2)))
                self.ui.tableResumenMensual.setItem(index, 4, QTableWidgetItem(self.locale.toString(float(dato['diferencia']), 'f', 2)))
                self.ui.tableResumenMensual.setItem(index, 5, QTableWidgetItem(self.locale.toString(int(dato['num_transacciones']))))
    
    def meses_combobox(self):
        self.ui.comboBoxMesGanancias.clear()
        self.ui.comboBoxMesGanancias.addItem("Todos")
        meses=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        num=1
        for mes in meses:
            self.ui.comboBoxMesGanancias.addItem(mes)
            index=self.ui.comboBoxMesGanancias.count()-1
            self.ui.comboBoxMesGanancias.setItemData(index, num, QtCore.Qt.ItemDataRole.UserRole)
            num+=1

    def graficar_ganancias(self):
        año = self.ui.spinBoxAñoGanancias.value()
        mes_seleccionado = self.ui.comboBoxMesGanancias.currentData(QtCore.Qt.ItemDataRole.UserRole)
        mes_para_db = mes_seleccionado if mes_seleccionado is not None else None
        datos = Caja.obtener_comparacion_cobros_gastos(año, mes_para_db)
        if self.ganancias_chart_view is not None:
            self.ui.verticalLayout_frame_grafico_ganancias.removeWidget(self.ganancias_chart_view)
            self.ganancias_chart_view.deleteLater()
            self.ganancias_chart_view = None
        self.ui.labelGraficoGananciasPlaceholder.hide()
        total_ganancias_gastos = datos['cobros'] + datos['gastos']
        if total_ganancias_gastos > 0:
            series = QPieSeries()
            cobros_slice = QPieSlice()
            cobros_slice.setValue(datos['cobros'])
            cobros_slice.setColor(QColor("#22E922")) 
            if total_ganancias_gastos > 0:
                percentage_cobros = (datos['cobros'] / total_ganancias_gastos) * 100
                cobros_slice.setLabel(f"Cobros: {self.locale.toString(datos['cobros'], 'f', 2)} ({percentage_cobros:.1f}%)")
            else:
                cobros_slice.setLabel(f"Cobros: {self.locale.toString(datos['cobros'], 'f', 2)}")
            cobros_slice.setLabelVisible(False)
            series.append(cobros_slice)
            gastos_slice = QPieSlice()
            gastos_slice.setValue(datos['gastos'])
            gastos_slice.setColor(QColor("#F85A48"))
            if total_ganancias_gastos > 0:
                percentage_gastos = (datos['gastos'] / total_ganancias_gastos) * 100
                gastos_slice.setLabel(f"Gastos: {self.locale.toString(datos['gastos'], 'f', 2)} ({percentage_gastos:.1f}%)")
            else:
                gastos_slice.setLabel(f"Gastos: {self.locale.toString(datos['gastos'], 'f', 2)}")
            gastos_slice.setLabelVisible(False) 
            series.append(gastos_slice)
            chart = QChart()
            chart.addSeries(series)
            if mes_para_db is None: 
                chart.setTitle(f"Comparación de Cobros y Gastos - Año {año}")
            else:
                mes_nombre = self.ui.comboBoxMesGanancias.currentText()
                chart.setTitle(f"Comparación de Cobros y Gastos - {mes_nombre} {año}")
            chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
            legend = chart.legend()
            legend.setVisible(True)
            legend.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.ganancias_chart_view = QChartView(chart)
            self.ganancias_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.ui.verticalLayout_frame_grafico_ganancias.addWidget(self.ganancias_chart_view)