import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QFileDialog, QLabel, QMessageBox, QDialog, QLineEdit, QFormLayout,
    QTextEdit, QHBoxLayout, QListWidget, QScrollArea, QGroupBox, QSpacerItem, QSizePolicy, QTabWidget, QDockWidget
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings
from data.db_manager import DatabaseManager
from PyQt5.QtCore import Qt

import os
from data.data_loader import DataLoader

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gerenciador de Planilhas')
        self.setGeometry(100, 100, 800, 600)  # Ajuste o tamanho se desejar
        self.loaded_data = None
        self.dark_mode = False  # Variável para controlar o tema

        # Cria objeto QSettings para salvamento persistente
        self.settings = QSettings("MinhaEmpresa", "GerenciadorPlanilhas")
        
        self.db_manager = DatabaseManager()
        self.initUI()
        self.load_settings()

    def initUI(self):
        """Configura a interface principal utilizando QTabWidget e adiciona ícones aos botões."""
        # Criando o QTabWidget principal
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # =============================
        # Aba "Home" - Interface Principal
        # =============================
        home_tab = QWidget()
        home_layout = QVBoxLayout(home_tab)
        
        # Status
        self.status_label = QLabel("Status: Nenhuma planilha carregada.", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(self.status_label)
        
        # Grupo de Planilhas
        spreadsheet_group = QGroupBox("Planilhas")
        spreadsheet_layout = QVBoxLayout()
        
        self.connect_button = QPushButton('Conectar com Planilha Remota\n(console.cloud.google)', self)
        self.connect_button.setIcon(QIcon.fromTheme("network-server"))
        self.connect_button.clicked.connect(self.connect_remote_spreadsheet)
        spreadsheet_layout.addWidget(self.connect_button)
        
        self.load_button = QPushButton('Carregar Planilhas do Computador', self)
        self.load_button.setIcon(QIcon.fromTheme("document-open"))
        self.load_button.clicked.connect(self.load_local_spreadsheet)
        spreadsheet_layout.addWidget(self.load_button)
        
        self.remove_button = QPushButton('Remover Planilhas', self)
        self.remove_button.setIcon(QIcon.fromTheme("edit-delete"))
        self.remove_button.clicked.connect(self.remove_spreadsheet)
        spreadsheet_layout.addWidget(self.remove_button)
        
        self.template_button = QPushButton('Baixar Template', self)
        self.template_button.setIcon(QIcon.fromTheme("document-save-as"))
        self.template_button.clicked.connect(self.download_template)
        spreadsheet_layout.addWidget(self.template_button)
        
        spreadsheet_group.setLayout(spreadsheet_layout)
        home_layout.addWidget(spreadsheet_group)
        
        # Botões de Análise e IA
        self.analyze_button = QPushButton('Analisar Dados', self)
        self.analyze_button.setIcon(QIcon.fromTheme("view-statistics"))
        self.analyze_button.clicked.connect(self.show_analysis)
        home_layout.addWidget(self.analyze_button)
        
        self.ai_button = QPushButton('Conectar IA Generativa', self)
        self.ai_button.setIcon(QIcon.fromTheme("system-run"))
        self.ai_button.clicked.connect(self.show_ai_config)
        home_layout.addWidget(self.ai_button)
        
        # Grupo de Banco de Dados
        db_group = QGroupBox("Banco de Dados")
        db_layout = QHBoxLayout()
        self.connect_db_button = QPushButton('Conectar MongoDB', self)
        self.connect_db_button.setIcon(QIcon.fromTheme("network"))
        self.connect_db_button.clicked.connect(self.show_db_connection_dialog)
        db_layout.addWidget(self.connect_db_button)
        db_group.setLayout(db_layout)
        home_layout.addWidget(db_group)
        
        # Área de Upload para IA
        self.upload_frame = QWidget()
        self.upload_frame.setVisible(False)
        upload_layout = QVBoxLayout()
        upload_info = QLabel("Faça upload de arquivos para análise qualitativa da IA")
        upload_layout.addWidget(upload_info)
        self.file_list = QListWidget()
        upload_layout.addWidget(self.file_list)
        upload_buttons = QHBoxLayout()
        add_file_btn = QPushButton("Adicionar Arquivo")
        add_file_btn.setIcon(QIcon.fromTheme("list-add"))
        add_file_btn.clicked.connect(self.add_file_for_analysis)
        upload_buttons.addWidget(add_file_btn)
        remove_file_btn = QPushButton("Remover Arquivo")
        remove_file_btn.setIcon(QIcon.fromTheme("list-remove"))
        remove_file_btn.clicked.connect(self.remove_file_from_analysis)
        upload_buttons.addWidget(remove_file_btn)
        upload_layout.addLayout(upload_buttons)
        self.upload_frame.setLayout(upload_layout)
        home_layout.addWidget(self.upload_frame)
        
        # Controles de Tema e Upload
        control_layout = QHBoxLayout()
        self.toggle_theme_btn = QPushButton("Alternar Tema", self)
        self.toggle_theme_btn.setIcon(QIcon.fromTheme("preferences-desktop-theme"))
        self.toggle_theme_btn.clicked.connect(self.toggle_theme)
        control_layout.addWidget(self.toggle_theme_btn)
        
        self.toggle_upload_btn = QPushButton("Área de Upload para IA", self)
        self.toggle_upload_btn.setIcon(QIcon.fromTheme("folder"))
        self.toggle_upload_btn.clicked.connect(self.toggle_upload_area)
        control_layout.addWidget(self.toggle_upload_btn)
        
        # Botão de Configurações Gerais
        self.settings_btn = QPushButton("⚙️ Configurações")
        self.settings_btn.setIcon(QIcon.fromTheme("preferences-system"))
        self.settings_btn.clicked.connect(self.show_settings_dialog)
        control_layout.addWidget(self.settings_btn)
        
        home_layout.addLayout(control_layout)
        home_layout.addStretch()
        
        # Adiciona a aba "Home"
        self.tabs.addTab(home_tab, "Home")
        
        
        # =============================
        # Aba "Configurações" - Geral
        # =============================
        settings_tab = QWidget()
        settings_layout = QFormLayout(settings_tab)
        
        # Exemplo de configuração persistente: Nome do aplicativo e Modelo de IA
        self.app_name_input = QLineEdit()
        settings_layout.addRow("Nome do Aplicativo:", self.app_name_input)
        
        self.default_model_input = QLineEdit()
        settings_layout.addRow("Modelo Padrão IA:", self.default_model_input)
        
        save_settings_btn = QPushButton("Salvar Configurações")
        save_settings_btn.setIcon(QIcon.fromTheme("document-save"))
        save_settings_btn.clicked.connect(self.save_settings)
        settings_layout.addRow(save_settings_btn)
        
        self.tabs.addTab(settings_tab, "Configurações Gerais")


    def show_settings_dialog(self):
        """Exibe um diálogo modal para configurações adicionais, se necessário."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Configurações Adicionais")
        layout = QFormLayout(dialog)
        
        api_key_input = QLineEdit()
        api_key_input.setEchoMode(QLineEdit.Password)
        layout.addRow("API Key:", api_key_input)
        
        model_input = QLineEdit()
        model_input.setText("gpt-3.5-turbo")
        layout.addRow("Modelo:", model_input)
        
        prompt_input = QTextEdit()
        prompt_input.setPlaceholderText("Insira um prompt personalizado para análise...")
        layout.addRow("Prompt:", prompt_input)
        
        btn_layout = QHBoxLayout()
        save_button = QPushButton("Salvar")
        save_button.setIcon(QIcon.fromTheme("document-save"))
        cancel_button = QPushButton("Cancelar")
        cancel_button.setIcon(QIcon.fromTheme("dialog-cancel"))
        btn_layout.addWidget(save_button)
        btn_layout.addWidget(cancel_button)
        layout.addRow(btn_layout)
        
        # Se necessário, conecte a lógica de salvamento deste diálogo
        save_button.clicked.connect(lambda: (
            QMessageBox.information(self, "Sucesso", "Configurações da IA salvas com sucesso!"),
            dialog.accept()
        ))
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec_()

    def load_settings(self):
        """Carrega as configurações persistentes no início."""
        self.dark_mode = self.settings.value("dark_mode", False, type=bool)
        if self.dark_mode:
            self.toggle_theme()  # Aplica o tema escuro se necessário
        
        # Exemplo: Carrega valores das abas de configurações
        self.app_name_input.setText(self.settings.value("app_name", "Gerenciador de Planilhas"))
        self.default_model_input.setText(self.settings.value("default_model", "gpt-3.5-turbo"))
    
    def save_settings(self):
        """Salva as configurações persistentes quando acionado (na aba de Configurações Gerais ou fechamento)."""
        self.settings.setValue("app_name", self.app_name_input.text())
        self.settings.setValue("default_model", self.default_model_input.text())
        # Você pode incluir outras configurações conforme necessário
        
        QMessageBox.information(self, "Configurações", "Configurações salvas com sucesso!")
    
    def closeEvent(self, event):
        """Salva as configurações ao fechar a aplicação."""
        self.save_settings()
        event.accept()
        
    def toggle_upload_area(self):
        """Alterna a visibilidade da área de upload."""
        self.upload_frame.setVisible(not self.upload_frame.isVisible())
        
    def add_file_for_analysis(self):
        """Adiciona um novo arquivo à lista de análise."""
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar Arquivos para Análise",
            "",
            "Arquivos de Texto (*.txt *.doc *.docx *.pdf);;Todos os Arquivos (*)",
            options=options
        )
        
        for file in files:
            self.file_list.addItem(file)

    def toggle_theme(self):
        """Alterna entre tema claro e escuro e salva a escolha nas configurações persistentes."""
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow, QWidget { background-color: #333; color: #fff; }
                QPushButton { 
                    background-color: #555; 
                    color: #fff;
                    border: 1px solid #777;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:hover { background-color: #666; }
                QLabel { color: #fff; }
            """)
        else:
            self.setStyleSheet("")
        
        # Salva o estado do tema
        self.settings.setValue("dark_mode", self.dark_mode)
            
    def remove_file_from_analysis(self):
        """Remove o arquivo selecionado da lista."""
        current_item = self.file_list.currentItem()
        if current_item:
            self.file_list.takeItem(self.file_list.row(current_item))
    def show_ai_config(self):
        """Mostra diálogo para configurar a conexão com IA generativa."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Configurar IA Generativa")
        
        layout = QFormLayout()
        
        # Campo para API Key
        api_key = QLineEdit()
        api_key.setEchoMode(QLineEdit.Password)
        layout.addRow("API Key:", api_key)
        
        # Campo para seleção do modelo
        model = QLineEdit()
        model.setText("gpt-3.5-turbo")
        layout.addRow("Modelo:", model)
        
        # Campo para prompt personalizado
        prompt = QTextEdit()
        prompt.setPlaceholderText("Insira um prompt personalizado para análise...")
        layout.addRow("Prompt:", prompt)
        
        # Botões
        buttons = QVBoxLayout()
        save_button = QPushButton("Salvar")
        cancel_button = QPushButton("Cancelar")
        
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)
        
        dialog.setLayout(layout)
        
        # Conecta os botões
        save_button.clicked.connect(lambda: self.save_ai_config(dialog, api_key.text(), model.text(), prompt.toPlainText()))
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec_()
    def save_ai_config(self, dialog, api_key, model, prompt):
        """Salva as configurações da IA e inicia a análise."""
        try:
            if not api_key:
                raise ValueError("API Key é obrigatória")
                
            # Aqui você pode adicionar a lógica para salvar as configurações
            # e iniciar a análise com a IA
            
            QMessageBox.information(self, "Sucesso", "Configurações da IA salvas com sucesso!")
            dialog.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar configurações:\n{e}")
    def show_db_connection_dialog(self):
        """Mostra diálogo para configurar conexão com MongoDB."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Configurar Conexão MongoDB")
        
        layout = QFormLayout()
        
        # Campos para conexão
        connection_string = QLineEdit()
        connection_string.setPlaceholderText("mongodb://localhost:27017")
        layout.addRow("String de Conexão:", connection_string)
        
        database_name = QLineEdit()
        database_name.setPlaceholderText("nome_do_banco")
        layout.addRow("Nome do Banco:", database_name)
        
        # Botões
        buttons = QHBoxLayout()
        connect_button = QPushButton("Conectar")
        cancel_button = QPushButton("Cancelar")
        
        buttons.addWidget(connect_button)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)
        
        dialog.setLayout(layout)
        
        # Conecta os botões
        connect_button.clicked.connect(
            lambda: self.connect_to_database(
                dialog, 
                connection_string.text(), 
                database_name.text()
            )
        )
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec_()
    def connect_to_database(self, dialog, connection_string, database_name):
        """Estabelece conexão com o MongoDB."""
        try:
            if not connection_string or not database_name:
                raise ValueError("Todos os campos são obrigatórios")
                
            if self.db_manager.connect(connection_string, database_name):
                QMessageBox.information(
                    self, 
                    "Sucesso", 
                    "Conexão estabelecida com sucesso!"
                )
                dialog.accept()
            else:
                raise ConnectionError("Não foi possível estabelecer conexão")
                
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Erro", 
                f"Erro ao conectar com o banco:\n{e}"
            )
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
            dashboard = Dashboard(self.loaded_data, self)
            dashboard.set_theme(self.dark_mode)
            
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

    def create_main_widget(self):
        """Cria e retorna o widget principal da janela."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Recria todos os widgets da interface principal
        self.initUI()
        
        # Retorna o widget principal
        return widget