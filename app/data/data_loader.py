import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
class DataLoader:
    def __init__(self, file_path=None, google_sheet_url=None, credentials_path="credentials.json"):
        """
        Inicializa o DataLoader.
        Parâmetros:
            file_path (str): Caminho para um arquivo local (CSV, TXT, Excel).
            google_sheet_url (str): URL da planilha do Google Sheets.
            credentials_path (str): Caminho para o arquivo JSON de credenciais da conta de serviço do Google.
        """
        self.file_path = file_path
        self.google_sheet_url = google_sheet_url
        self.credentials_path = credentials_path
    def load_data(self):
        """Carrega os dados de arquivos CSV, TXT, Excel ou Google Sheets com verificação de formato."""
        if self.file_path:
            try:
                if self.file_path.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(self.file_path)
                elif self.file_path.endswith(('.csv', '.txt')):
                    df = pd.read_csv(self.file_path)
                else:
                    raise ValueError("Formato de arquivo não suportado.")
                # Verificação de estrutura: por exemplo, colunas obrigatórias
                expected_columns = ["curso", "turno", "semestre", "ano"]
                missing_cols = [col for col in expected_columns if col not in df.columns]
                if missing_cols:
                    raise ValueError(f"Colunas faltantes no arquivo: {missing_cols}")
                return df
            except Exception as e:
                raise ValueError(f"Erro ao processar o arquivo: {e}")
        elif self.google_sheet_url:
            return self._load_from_google_sheets()
        else:
            raise ValueError("Nenhuma fonte de dados fornecida.")
    def _load_from_google_sheets(self):
        """Carrega os dados a partir de uma planilha do Google Sheets."""
        try:
            # Define os escopos necessários
            scopes = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            # Cria as credenciais da conta de serviço a partir do arquivo JSON
            creds = Credentials.from_service_account_file(self.credentials_path, scopes=scopes)
            # Autoriza o cliente do gspread com as credenciais
            client = gspread.authorize(creds)
            # Abre a planilha a partir da URL e seleciona a primeira aba (sheet1)
            sheet = client.open_by_url(self.google_sheet_url).sheet1
            # Obtém os dados da planilha como uma lista de dicionários
            data = sheet.get_all_records()
            if not data:
                raise ValueError("Nenhum dado encontrado na planilha.")
            # Converte a lista de dicionários em um DataFrame do pandas
            df = pd.DataFrame(data)
            # Verificação de estrutura: Colunas obrigatórias
            expected_columns = ["curso", "turno", "semestre", "ano"]
            missing_cols = [col for col in expected_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Colunas faltantes na planilha: {missing_cols}")
            return df
        except Exception as e:
            raise ValueError(f"Erro ao carregar dados do Google Sheets: {e}")