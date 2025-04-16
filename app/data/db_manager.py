import os
import json
import logging
import time
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
# Configuração básica do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self):
        self.client = None
        self.db = None
        # Estrutura simples para cache, mapeando (collection_name, query_key) -> resultado
        self.cache = {}

        # Define schemas/estruturas para as coleções
        self.schemas = {
            'evasao_dados': {
                'curso': str,
                'turno': str,
                'semestre': int,
                'ano': int,
                'desistentes': {
                    '1C': int,
                    '2C': int,
                    '3C': int,
                    '4C': int,
                    '5C': int,
                    '6C': int
                },
                'metadata': {
                    'data_insercao': datetime,
                    'ultima_atualizacao': datetime,
                    'fonte_dados': str
                }
            },
            'analises': {
                'tipo_analise': str,
                'parametros': dict,
                'resultados': dict,
                'data_analise': datetime,
                'metadata': {
                    'versao_modelo': str,
                    'precisao': float,
                    'observacoes': str
                }
            },
            'previsoes': {
                'curso': str,
                'periodo': {
                    'ano': int,
                    'semestre': int
                },
                'valor_previsto': float,
                'intervalo_confianca': {
                    'inferior': float,
                    'superior': float
                },
                'metadata': {
                    'modelo_usado': str,
                    'data_previsao': datetime,
                    'parametros_modelo': dict
                }
            }
        }

    def connect(self, connection_string, database_name, max_retries=3, retry_delay=2):
        """
        Estabelece conexão com o MongoDB com suporte a reconexão automática.
        
        Args:
            connection_string (str): String de conexão do MongoDB
            database_name (str): Nome do banco de dados
            max_retries (int): Número máximo de tentativas de reconexão
            retry_delay (int): Tempo de espera entre tentativas em segundos
            
        Returns:
            bool: True se conectado com sucesso, False caso contrário
        """
        attempts = 0
        while attempts < max_retries:
            try:
                if self.client is not None:
                    self.client.close()
                
                self.client = MongoClient(connection_string, 
                                       serverSelectionTimeoutMS=5000,
                                       connectTimeoutMS=5000)
                self.db = self.client[database_name]
                
                # Testa a conexão
                self.client.admin.command('ping')
                logging.info("Conectado com sucesso ao MongoDB!")
                return True
                
            except ConnectionFailure as e:
                attempts += 1
                if attempts < max_retries:
                    logging.warning(f"Tentativa {attempts} falhou. Tentando reconectar em {retry_delay} segundos...")
                    time.sleep(retry_delay)
                else:
                    logging.error(f"Falha na conexão após {max_retries} tentativas: {e}")
                    return False
                    
            except Exception as e:
                logging.error(f"Erro inesperado ao conectar: {e}")
                return False
    def disconnect(self):
        """Fecha a conexão com o MongoDB e limpa o cache."""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            self.cache.clear()
            logging.info("Desconectado e cache limpo.")

    # ----------------- Validação de Schema -----------------
    def _validate_document(self, collection_name, document, schema=None, path=""):
        """
        Verifica recursivamente se o documento segue o schema esperado.
        Lança ValueError caso haja inconsistência.
        """
        if collection_name not in self.schemas:
            # Sem schema definido para essa coleção, assume que está ok.
            return

        # Se nenhum schema foi passado, obtém o schema da coleção
        if schema is None:
            schema = self.schemas[collection_name]

        for key, expected_type in schema.items():
            full_key = f"{path}.{key}" if path else key
            if key not in document:
                raise ValueError(f"Campo obrigatório '{full_key}' ausente.")
            
            valor = document[key]
            # Se o expected_type for um dicionário, assumimos que há aninhamento
            if isinstance(expected_type, dict):
                if not isinstance(valor, dict):
                    raise ValueError(f"Campo '{full_key}' deve ser um dicionário.")
                self._validate_document(collection_name, valor, schema=expected_type, path=full_key)
            else:
                # Permite valor None ou do tipo esperado
                if valor is not None and not isinstance(valor, expected_type):
                    raise ValueError(
                        f"Campo '{full_key}' deve ser do tipo {expected_type.__name__}, "
                        f"mas foi fornecido do tipo {type(valor).__name__}."
                    )

    # ----------------- Funções CRUD -----------------
    def insert_data(self, collection_name, data):
        """
        Insere dados na coleção.
        Aceita: dicionário para um único documento ou lista de documentos.
        Valida o documento contra o schema definido e invalida o cache da coleção.
        """
        self._check_connection()
        collection = self.db[collection_name]
        # Invalida cache para essa coleção
        self._invalidate_cache(collection_name)
        
        # Se for lista, valida cada documento
        if isinstance(data, list):
            for doc in data:
                self._validate_document(collection_name, doc)
            result = collection.insert_many(data)
            logging.info(f"{len(result.inserted_ids)} documentos inseridos.")
            return result.inserted_ids
        else:
            self._validate_document(collection_name, data)
            result = collection.insert_one(data)
            logging.info("Documento inserido.")
            return result.inserted_id

    def get_data(self, collection_name, query={}):
        """
        Recupera dados da coleção com suporte a cache.
        Se a mesma consulta já foi realizada, retorna os dados do cache.
        """
        self._check_connection()
        # Gera uma chave simples para o cache
        query_key = self._generate_cache_key(query)
        cache_key = (collection_name, query_key)
        if cache_key in self.cache:
            logging.info("Retornando dados do cache.")
            return self.cache[cache_key]

        collection = self.db[collection_name]
        data = list(collection.find(query))
        # Armazena no cache
        self.cache[cache_key] = data
        logging.info("Dados recuperados do banco e armazenados no cache.")
        return data

    def update_data(self, collection_name, query, update_values, many=False):
        """
        Atualiza documentos na coleção.
        Se many=True, atualiza vários documentos; senão, atualiza apenas um.
        Valida os dados atualizados e invalida o cache da coleção.
        """
        self._check_connection()
        collection = self.db[collection_name]
        self._invalidate_cache(collection_name)

        # Se o schema existir e os dados atualizados forem um conjunto de campos,
        # podemos validar cada campo que está sendo atualizado.
        schema = self.schemas.get(collection_name, {})
        for field, value in update_values.items():
            if field in schema:
                expected_type = schema[field]
                if isinstance(expected_type, dict):
                    if not isinstance(value, dict):
                        raise ValueError(f"Campo '{field}' deve ser um dicionário.")
                    # Validação recursiva para campos aninhados
                    self._validate_document(collection_name, value, schema=expected_type, path=field)
                else:
                    if value is not None and not isinstance(value, expected_type):
                        raise ValueError(
                            f"Campo '{field}' deve ser do tipo {expected_type.__name__}, "
                            f"mas foi fornecido do tipo {type(value).__name__}."
                        )

        if many:
            result = collection.update_many(query, {'$set': update_values})
            logging.info(f"{result.modified_count} documentos atualizados.")
        else:
            result = collection.update_one(query, {'$set': update_values})
            logging.info(f"{result.modified_count} documento atualizado.")
        return result.modified_count

    def delete_data(self, collection_name, query, many=False):
        """
        Remove documentos da coleção.
        Se many=True, remove vários documentos; senão, remove apenas um.
        Invalida o cache da coleção.
        """
        self._check_connection()
        collection = self.db[collection_name]
        self._invalidate_cache(collection_name)
        if many:
            result = collection.delete_many(query)
            logging.info(f"{result.deleted_count} documentos removidos.")
        else:
            result = collection.delete_one(query)
            logging.info(f"{result.deleted_count} documento removido.")
        return result.deleted_count

    # ----------------- Funcionalidades de Cache -----------------
    def _generate_cache_key(self, query):
        """
        Gera uma chave hashável para um dicionário de consulta.
        Para queries simples, utiliza uma tupla com os itens ordenados.
        """
        return tuple(sorted(query.items()))

    def _invalidate_cache(self, collection_name):
        """Remove do cache todas as entradas relacionadas a uma coleção."""
        keys_to_invalidate = [key for key in self.cache if key[0] == collection_name]
        for key in keys_to_invalidate:
            del self.cache[key]
        logging.info(f"Cache invalidado para a coleção '{collection_name}'.")

    # ----------------- Funções de Backup -----------------
    def backup_db(self, backup_dir="backup"):
        """
        Realiza backup de todas as coleções do banco de dados.
        Exporta os dados de cada coleção para um arquivo JSON na pasta especificada.
        """
        self._check_connection()
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            logging.info(f"Pasta de backup '{backup_dir}' criada.")

        collections = self.db.list_collection_names()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for coll in collections:
            data = list(self.db[coll].find())
            # Converte ObjectId e datas para serializáveis se necessário
            for doc in data:
                doc['_id'] = str(doc['_id'])
            backup_file = os.path.join(backup_dir, f"{coll}_backup_{timestamp}.json")
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logging.info(f"Backup da coleção '{coll}' salvo em '{backup_file}'.")

    # ----------------- Funções de Migração de Dados -----------------
    def migrate_data(self, collection_name, migration_fn, query={}):
        """
        Aplica uma função de migração aos documentos de uma coleção.
        migration_fn: função que recebe um documento e retorna o documento migrado.
        query: condição para selecionar os documentos que serão migrados.
        
        A função percorre todos os documentos que correspondem à query,
        aplica a migração e atualiza o documento na coleção.
        """
        self._check_connection()
        collection = self.db[collection_name]
        documents = list(collection.find(query))
        count = 0
        for doc in documents:
            migrated_doc = migration_fn(doc)
            # Validação opcional pode ser aplicada no documento migrado
            self._validate_document(collection_name, migrated_doc)
            result = collection.update_one({'_id': doc['_id']}, {'$set': migrated_doc})
            if result.modified_count:
                count += 1
        self._invalidate_cache(collection_name)
        logging.info(f"Migração aplicada em {count} documentos da coleção '{collection_name}'.")
        return count

    # ----------------- Helpers -----------------
    def _check_connection(self):
        """Verifica se a conexão com o banco de dados foi estabelecida."""
        if not self.db:
            raise ConnectionError("Não conectado ao banco de dados.")