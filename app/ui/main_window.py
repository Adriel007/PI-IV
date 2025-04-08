import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QFileDialog, QLabel, QMessageBox, QDialog, QLineEdit, QFormLayout
)
from PyQt5.QtCore import Qt
import os
from data.data_loader import DataLoader

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gerenciador de Planilhas')
        self.setGeometry(100, 100, 400, 300)
        self.loaded_data = None  # Armazena o DataFrame carregado
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Label de status
        self.status_label = QLabel("Status: Nenhuma planilha carregada.", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Botões
        self.connect_button = QPushButton('Conectar com Planilha Remota\n(console.cloud.google)', self)
        self.connect_button.clicked.connect(self.connect_remote_spreadsheet)
        layout.addWidget(self.connect_button)

        self.load_button = QPushButton('Carregar Planilhas do Computador', self)
        self.load_button.clicked.connect(self.load_local_spreadsheet)
        layout.addWidget(self.load_button)

        self.remove_button = QPushButton('Remover Planilhas', self)
        self.remove_button.clicked.connect(self.remove_spreadsheet)
        layout.addWidget(self.remove_button)
        self.template_button = QPushButton('Baixar Template', self)
        self.template_button.clicked.connect(self.download_template)
        layout.addWidget(self.template_button)
        # Widget central
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.analyze_button = QPushButton('Analisar Dados', self)
        self.analyze_button.clicked.connect(self.show_analysis)
        layout.addWidget(self.analyze_button)
    def download_template(self):
        """Permite ao usuário baixar um template vazio com as colunas necessárias."""
        try:
            options = QFileDialog.Options()
            file_name, file_type = QFileDialog.getSaveFileName(
                self,
                "Salvar Template",
                "",
                "CSV (*.csv);;Excel (*.xlsx)",
                options=options
            )
            
            if file_name:
                # Colunas obrigatórias do template
                columns = ["curso", "turno", "semestre", "ano", "1° C", "2° C", "3° C", "4° C", "5° C", "6° C"]
                
                if file_name.endswith('.csv'):
                    import pandas as pd
                    # Criar DataFrame vazio com as colunas
                    df = pd.DataFrame(columns=columns)
                    df.to_csv(file_name, index=False)
                elif file_name.endswith('.xlsx'):
                    import pandas as pd
                    # Criar DataFrame vazio com as colunas
                    df = pd.DataFrame(columns=columns)
                    df.to_excel(file_name, index=False)
                    
                self.status_label.setText(f"Template salvo com sucesso em: {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar template:\n{e}")

    def _show_auth_dialog(self):
        """Mostra um diálogo para inserir URL da planilha e caminho das credenciais."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Conectar ao Google Sheets")
        
        # Layout do formulário
        layout = QFormLayout()
        
        # Campos de entrada
        sheet_url = QLineEdit()
        credentials_path = QLineEdit()
        
        # Adiciona campos ao layout
        layout.addRow("URL da Planilha:", sheet_url)
        layout.addRow("Caminho das Credenciais:", credentials_path)
        
        # Botões
        buttons = QVBoxLayout()
        ok_button = QPushButton("Conectar")
        cancel_button = QPushButton("Cancelar")
        
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)
        
        dialog.setLayout(layout)
        
        # Conecta os botões
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        
        # Executa o diálogo
        if dialog.exec_() == QDialog.Accepted:
            return sheet_url.text(), credentials_path.text()
        return None
    
    def show_analysis(self):
        """Exibe análises e gráficos dos dados carregados."""
        if self.loaded_data is None:
            QMessageBox.warning(self, "Aviso", "Carregue uma planilha primeiro!")
            return
        try:
            from ui.charts import Dashboard
            from prediction.prediction import Predictor
            
            # Criar dashboard com gráficos
            dashboard = Dashboard(self.loaded_data)
            
            # Definir o dashboard como widget central
            self.setCentralWidget(dashboard)
            
            # Realizar previsões
            predictor = Predictor(self.loaded_data)
            future_years = range(2024, 2027)  # Próximos 3 anos
            predictor.plot_predictions(future_years)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar análises:\n{e}")

    def load_local_spreadsheet(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Selecione a Planilha",
            "",
            "Arquivos de Dados (*.csv *.txt *.xls *.xlsx);;Todos os Arquivos (*)",
            options=options
        )
        if file:
            try:
                loader = DataLoader(file_path=file)
                self.loaded_data = loader.load_data()
                self.status_label.setText(f"Status: {os.path.basename(file)} carregada com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao carregar o arquivo:\n{e}")
                self.status_label.setText("Status: Falha no carregamento da planilha.")

    def remove_spreadsheet(self):
        # Confirmação para evitar remoção acidental
        reply = QMessageBox.question(
            self, 'Confirmação',
            "Você tem certeza que deseja remover a planilha carregada?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                if self.loaded_data is None:
                    raise ValueError("Nenhuma planilha carregada para remoção.")
                self.loaded_data = None
                self.status_label.setText("Status: Planilha removida com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao remover a planilha:\n{e}")
                self.status_label.setText("Status: Falha na remoção da planilha.")
    def connect_remote_spreadsheet(self):
        """Conecta com uma planilha remota do Google Sheets."""
        try:
            # Mostrar diálogo para obter URL e credenciais
            auth_result = self._show_auth_dialog()
            if auth_result:
                sheet_url, credentials_path = auth_result
                
                # Criar instância do DataLoader com as credenciais do Google Sheets
                loader = DataLoader(
                    google_sheet_url=sheet_url,
                    credentials_path=credentials_path
                )
                
                # Carregar os dados
                self.loaded_data = loader.load_data()
                self.status_label.setText(f"Status: Planilha remota conectada com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao conectar com planilha remota:\n{e}")
            self.status_label.setText("Status: Falha na conexão com planilha remota.")