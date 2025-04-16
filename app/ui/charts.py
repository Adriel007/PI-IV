import pandas as pd
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QPushButton, 
                           QScrollArea, QCheckBox, QGridLayout)
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class Dashboard(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.df = data if data is not None else pd.DataFrame()
        self.selected_courses = set(self.df["curso"].unique())
        self.colors = plt.cm.Set3(np.linspace(0, 1, len(self.df["curso"].unique())))
        self.dark_mode = False
        self.initUI()
    def initUI(self):
        if self.df.empty:
            print("⚠️ Nenhum dado carregado no Dashboard.")
            return
        layout = QVBoxLayout()
        
        # Botão de voltar
        back_button = QPushButton("Voltar ao Menu")
        back_button.clicked.connect(self.return_to_menu)
        layout.addWidget(back_button)
        
        # Filtro Avançado: seleção de ano
        from PyQt5.QtWidgets import QComboBox, QLabel, QHBoxLayout
        filter_layout = QHBoxLayout()
        year_label = QLabel("Filtrar por ano:")
        self.year_filter = QComboBox()
        self.year_filter.addItem("Todos os anos")
        self.year_filter.addItems([str(ano) for ano in sorted(self.df["ano"].unique())])
        self.year_filter.currentIndexChanged.connect(self.updateCharts)
        filter_layout.addWidget(year_label)
        filter_layout.addWidget(self.year_filter)
        layout.addLayout(filter_layout)
        
        # Área de seleção de cursos
        scroll = QScrollArea()
        course_widget = QWidget()
        course_layout = QGridLayout()
        
        for i, curso in enumerate(sorted(self.df["curso"].unique())):
            cb = QCheckBox(curso)
            cb.setChecked(True)
            cb.stateChanged.connect(self.updateCharts)
            course_layout.addWidget(cb, i // 3, i % 3)
        
        course_widget.setLayout(course_layout)
        scroll.setWidget(course_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        # Container para gráficos: usa QTabWidget para organizar os gráficos
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Botão para exportar gráficos
        export_btn = QPushButton("Exportar Gráficos")
        export_btn.clicked.connect(self.export_charts)
        layout.addWidget(export_btn)
        
        self.setLayout(layout)
        self.updateCharts()
        
    def updateCharts(self):
        # Atualiza lista de cursos selecionados
        self.selected_courses = set()
        for cb in self.findChildren(QCheckBox):
            if cb.isChecked():
                self.selected_courses.add(cb.text())
        
        # Filtra os dados inicialmente pela seleção de cursos
        df_filtered = self.df[self.df["curso"].isin(self.selected_courses)]
        
        # Filtro avançado: aplicar filtro por ano, se selecionado
        selected_year = self.year_filter.currentText() if hasattr(self, "year_filter") else "Todos os anos"
        if selected_year != "Todos os anos":
            df_filtered = df_filtered[df_filtered["ano"] == int(selected_year)]
        
        # Limpa tabs existentes
        while self.tab_widget.count() > 0:
            self.tab_widget.removeTab(0)
            
        # Recria gráficos com dados filtrados
        if not df_filtered.empty:
            # Gráfico de Pizza
            pie_chart = self.create_pie_chart(df_filtered)
            pie_view = QChartView(pie_chart)
            pie_view.setRenderHint(QPainter.Antialiasing)
            self.tab_widget.addTab(pie_view, "Distribuição por Curso")
            
            # Gráfico de Barras
            bar_chart = self.create_bar_chart(df_filtered)
            bar_view = QChartView(bar_chart)
            bar_view.setRenderHint(QPainter.Antialiasing)
            self.tab_widget.addTab(bar_view, "Desistências por Ano")
            
            # Gráfico de Linha com Matplotlib
            line_chart = self.create_line_chart(df_filtered)
            self.tab_widget.addTab(line_chart, "Tendência Temporal")

    def create_pie_chart(self, df):
        series = QPieSeries()
        for i, curso in enumerate(sorted(df["curso"].unique())):
            count = df[df["curso"] == curso].shape[0]
            slice = series.append(curso, count)
            # Define a cor do slice usando a paleta já carregada
            color = self.colors[list(self.df["curso"].unique()).index(curso)]
            slice.setBrush(QColor(plt.matplotlib.colors.rgb2hex(color)))
        
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Distribuição de Cursos")
        chart.legend().setAlignment(Qt.AlignRight)
        return chart
    def create_bar_chart(self, df):
        chart = QChart()
        series = QBarSeries()
        
        anos = sorted(df["ano"].unique())
        for i, ano in enumerate(anos):
            bar_set = QBarSet(str(ano))
            # Soma as desistências considerando as colunas a partir da 5ª coluna
            desistentes = df[df["ano"] == ano].iloc[:, 4:].sum().sum()
            bar_set.append(desistentes)
            color = self.colors[i % len(self.colors)]
            bar_set.setColor(QColor(plt.matplotlib.colors.rgb2hex(color)))
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
        
    def create_line_chart(self, df):
        # Cria gráfico de linha usando Matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for i, curso in enumerate(sorted(df["curso"].unique())):
            dados_curso = df[df["curso"] == curso]
            desistentes_por_ano = dados_curso.groupby("ano").apply(lambda x: x.iloc[:, 4:].sum().sum())
            color = self.colors[list(self.df["curso"].unique()).index(curso)]
            ax.plot(desistentes_por_ano.index, desistentes_por_ano.values, 
                    label=curso, color=color, marker='o')
        
        ax.set_xlabel("Ano")
        ax.set_ylabel("Total de Desistências")
        ax.set_title("Tendência de Desistências por Curso")
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True)
        
        fig.tight_layout()
        canvas = FigureCanvas(fig)
        return canvas
    
    def export_charts(self):
        """Exporta os gráficos presentes nas abas para arquivos PNG ou PDF."""
        from PyQt5.QtWidgets import QFileDialog
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            title = self.tab_widget.tabText(i).replace(" ", "_")
            file_name, selected_filter = QFileDialog.getSaveFileName(
                self,
                f"Salvar {title}",
                f"{title}.png",
                "PNG (*.png);;PDF (*.pdf)"
            )
            if file_name:
                # Se o widget for QChartView, usamos grab() para capturar a imagem
                if hasattr(widget, "grab"):
                    pixmap = widget.grab()
                    pixmap.save(file_name)
                # Se for um canvas do Matplotlib (FigureCanvas), salva a figura diretamente
                elif hasattr(widget, "figure"):
                    widget.figure.savefig(file_name)

    
    def return_to_menu(self):
        """Retorna à tela principal."""
        self.parent().initUI()

    def set_theme(self, is_dark):
        """Aplica o tema escuro ou claro aos gráficos."""
        self.dark_mode = is_dark
        if is_dark:
            plt.style.use('dark_background')
            for chart_view in self.findChildren(QChartView):
                chart = chart_view.chart()
                chart.setBackgroundBrush(QColor("#333"))
                chart.setTitleBrush(QColor("#fff"))
                chart.legend().setLabelColor(QColor("#fff"))
        else:
            plt.style.use('default')
            for chart_view in self.findChildren(QChartView):
                chart = chart_view.chart()
                chart.setBackgroundBrush(QColor("#fff"))
                chart.setTitleBrush(QColor("#000"))
                chart.legend().setLabelColor(QColor("#000"))
        self.updateCharts()