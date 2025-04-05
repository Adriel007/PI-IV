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

        # Widget central
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.analyze_button = QPushButton('Analisar Dados', self)
        self.analyze_button.clicked.connect(self.show_analysis)
        layout.addWidget(self.analyze_button)
        # Widget central
        central_widget = QWidget(self)

    def connect_remote_spreadsheet(self):
        self.status_label.setText("Conectando com planilha remota...")
        try:
            # Mostra diálogo de autenticação
            auth_data = self._show_auth_dialog()
            if auth_data:
                sheet_url, credentials_path = auth_data
                # Tenta conectar com a planilha usando as credenciais fornecidas
                loader = DataLoader(google_sheet_url=sheet_url, credentials_path=credentials_path)
                self.loaded_data = loader.load_data()
                self.status_label.setText("Status: Planilha remota carregada com sucesso!")
            else:
                self.status_label.setText("Status: Conexão cancelada pelo usuário.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao conectar com planilha remota:\n{e}")
            self.status_label.setText("Status: Falha ao carregar planilha remota.")

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

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
