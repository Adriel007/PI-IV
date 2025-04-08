import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
class Dashboard(QWidget):
    def __init__(self, data):
        super().__init__()
        self.df = data if data is not None else pd.DataFrame()
        self.initUI()
    def initUI(self):
        if self.df.empty:
            print("⚠️ Nenhum dado carregado no Dashboard.")
            return
        layout = QVBoxLayout()
        tab_widget = QTabWidget()
        
        # Gráfico de Pizza
        pie_chart = self.create_pie_chart()
        tab_widget.addTab(QChartView(pie_chart), "Distribuição por Curso")
        
        # Gráfico de Barras
        bar_chart = self.create_bar_chart()
        tab_widget.addTab(QChartView(bar_chart), "Desistências por Ano")
        
        # Gráfico de Linha
        line_chart_widget = self.create_line_chart()
        tab_widget.addTab(line_chart_widget, "Tendência Temporal")
        
        layout.addWidget(tab_widget)
        self.setLayout(layout)
    def create_pie_chart(self):
        series = QPieSeries()
        for curso in self.df["curso"].unique():
            count = self.df[self.df["curso"] == curso].shape[0]
            series.append(curso, count)
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Distribuição de Cursos")
        return chart
    def create_bar_chart(self):
        chart = QChart()
        series = QBarSeries()
        
        anos = sorted(self.df["ano"].unique())
        for ano in anos:
            bar_set = QBarSet(str(ano))
            desistentes = self.df[self.df["ano"] == ano].iloc[:, 4:].sum().sum()
            bar_set.append(desistentes)
            series.append(bar_set)
        chart.addSeries(series)
        chart.setTitle("Desistências por Ano")
        
        axis_x = QBarCategoryAxis()
        axis_x.append(["Total"])
        chart.addAxis(axis_x, Qt.AlignBottom)
        
        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        return chart
    def create_line_chart(self):
        fig, ax = plt.subplots()
        
        for curso in self.df["curso"].unique():
            dados_curso = self.df[self.df["curso"] == curso]
            desistentes_por_ano = dados_curso.groupby("ano").apply(lambda x: x.iloc[:, 4:].sum().sum())

            ax.plot(desistentes_por_ano.index, desistentes_por_ano.values, label=curso)
        
        ax.set_xlabel("Ano")
        ax.set_ylabel("Total de Desistências")
        ax.set_title("Tendência de Desistências por Curso")
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        canvas = FigureCanvas(fig)
        return canvas