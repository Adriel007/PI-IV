import os
import pandas as pd
import gspread
import logging
from google.oauth2.service_account import Credentials
import pickle
import time

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataLoader:
    def __init__(self, file_path=None, google_sheet_url=None, credentials_path="credentials.json", cache_file="data_cache.pkl"):
        self.file_path = file_path
        self.google_sheet_url = google_sheet_url
        self.credentials_path = credentials_path
        self.cache_file = cache_file
        self.version = None

    def load_data(self):
        logging.info("Iniciando processo de carregamento de dados.")
        if self.file_path:
            logging.info(f"Carregando dados a partir do arquivo: {self.file_path}")
            try:
                if self.file_path.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(self.file_path)
                    logging.info("Arquivo Excel carregado com sucesso.")
                elif self.file_path.endswith(('.csv', '.txt')):
                    df = pd.read_csv(self.file_path)
                    logging.info("Arquivo CSV/TXT carregado com sucesso.")
                else:
                    raise ValueError("Formato de arquivo não suportado.")
                
                expected_columns = ["curso", "turno", "semestre", "ano"]
                missing_cols = [col for col in expected_columns if col not in df.columns]
                if missing_cols:
                    raise ValueError(f"Colunas faltantes no arquivo: {missing_cols}")

                logging.info("Estrutura do arquivo validada com sucesso.")
                return df
            except Exception as e:
                logging.error(f"Erro ao processar o arquivo: {e}")
                raise ValueError(f"Erro ao processar o arquivo: {e}")
        
        elif self.google_sheet_url:
            logging.info(f"Carregando dados a partir do Google Sheets: {self.google_sheet_url}")
            return self._load_from_google_sheets()
        else:
            logging.error("Nenhuma fonte de dados fornecida.")
            raise ValueError("Nenhuma fonte de dados fornecida.")

    def _load_from_google_sheets(self):
        try:
            if self._is_cache_valid():
                logging.info("Carregando dados do cache.")
                return self._load_from_cache()
            
            logging.info("Carregando dados do Google Sheets.")
            scopes = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = Credentials.from_service_account_file(self.credentials_path, scopes=scopes)
            client = gspread.authorize(creds)
            logging.info("Credenciais do Google autenticadas com sucesso.")

            sheet = client.open_by_url(self.google_sheet_url).sheet1
            data = sheet.get_all_records()

            if not data:
                raise ValueError("Nenhum dado encontrado na planilha.")

            df = pd.DataFrame(data)
            logging.info("Dados carregados da planilha com sucesso.")

            expected_columns = ["curso", "turno", "semestre", "ano"]
            missing_cols = [col for col in expected_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Colunas faltantes na planilha: {missing_cols}")
            
            logging.info("Estrutura da planilha validada com sucesso.")

            # Armazenando dados no cache
            self._store_in_cache(df)
            return df
        except Exception as e:
            logging.error(f"Erro ao carregar dados do Google Sheets: {e}")
            raise ValueError(f"Erro ao carregar dados do Google Sheets: {e}")

    def _is_cache_valid(self):
        if not os.path.exists(self.cache_file):
            return False

        try:
            with open(self.cache_file, 'rb') as cache_file:
                cache_data = pickle.load(cache_file)
                current_version = self._get_google_sheet_version()
                if cache_data['version'] != current_version:
                    logging.info("Versão da planilha alterada. Atualizando cache.")
                    return False
                return True
        except Exception as e:
            logging.error(f"Erro ao verificar a validade do cache: {e}")
            return False

    def _get_google_sheet_version(self):
        try:
            scopes = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = Credentials.from_service_account_file(self.credentials_path, scopes=scopes)
            client = gspread.authorize(creds)

            sheet = client.open_by_url(self.google_sheet_url).sheet1
            version = sheet.updated
            return version
        except Exception as e:
            logging.error(f"Erro ao obter a versão da planilha: {e}")
            return None

    def _load_from_cache(self):
        try:
            with open(self.cache_file, 'rb') as cache_file:
                cache_data = pickle.load(cache_file)
                return cache_data['data']
        except Exception as e:
            logging.error(f"Erro ao carregar dados do cache: {e}")
            raise ValueError("Erro ao carregar dados do cache.")
    
    def _store_in_cache(self, df):
        try:
            version = self._get_google_sheet_version()
            cache_data = {'data': df, 'version': version}
            with open(self.cache_file, 'wb') as cache_file:
                pickle.dump(cache_data, cache_file)
            logging.info("Dados armazenados no cache com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao armazenar dados no cache: {e}")
