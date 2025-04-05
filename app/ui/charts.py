import pandas as pd
from PyQt5.QtWidgets import QWidget
from PyQt5.QtChart import QChart, QChartView, QPieSeries

class Dashboard(QWidget):
    def __init__(self, data):
        super().__init__()
        self.df = data if data is not None else pd.DataFrame()  # Garante que self.df não seja None
        self.initUI()

    def initUI(self):
        if self.df.empty:
            print("⚠️ Nenhum dado carregado no Dashboard.")
            return  # Evita falhas ao tentar plotar dados vazios
        
        self.plot_data()

    def plot_data(self):
        """Gera um gráfico a partir dos dados."""
        if self.df.empty:
            print("⚠️ Nenhum dado disponível para plotar.")
            return

        # Exemplo: Gráfico de pizza da contagem de cursos
        series = QPieSeries()
        for curso in self.df["curso"].unique():
            count = self.df[self.df["curso"] == curso].shape[0]
            series.append(curso, count)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Distribuição de Cursos")

        chart_view = QChartView(chart)
        chart_view.setParent(self)
