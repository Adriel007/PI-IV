import pandas as pd

class DataProcessor:
    def __init__(self, df, matriculados_df=None):
        self.df = df
        self.matriculados_df = matriculados_df

    def clean_data(self):
        """Realiza a limpeza dos dados, tratando valores faltantes e anômalos."""
        # Preenche valores faltantes com 0 (ou outra estratégia adequada)
        self.df = self.df.fillna(0)
        # Converte colunas numéricas para o tipo correto, se presentes
        for col in ["semestre", "ano", "desistentes"]:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
        return self.df

    def calculate_dropout_rate(self):
        """Calcula a taxa de desistência por semestre, considerando o histórico e ciclos acadêmicos."""
        if self.matriculados_df is None:
            raise ValueError("Dados de matriculados não fornecidos.")
        required_columns = ["curso", "turno", "semestre", "ano", "entradas"]
        for col in required_columns:
            if col not in self.df.columns or col not in self.matriculados_df.columns:
                raise ValueError(f"Coluna necessária '{col}' não encontrada.")
        df_merged = self.df.merge(self.matriculados_df, on=["curso", "turno", "semestre", "ano"])
        # Soma os desistentes em todas as colunas de desistência (supondo que estas estejam a partir da 5ª coluna até a penúltima)
        df_merged["total_desistentes"] = df_merged.iloc[:, 4:-1].sum(axis=1)
        # Calcula a taxa de forma segura, evitando divisão por zero
        df_merged["taxa_desistencia"] = df_merged.apply(
            lambda row: row["total_desistentes"] / row["entradas"] if row["entradas"] else 0, axis=1)
        return df_merged[["curso", "semestre", "ano", "taxa_desistencia"]]
