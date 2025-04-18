import pandas as pd

# Caminho do arquivo
arquivo_excel = "dados_originais.xlsx"

# Leitura com multi-index nas colunas (duas linhas de cabeçalho)
df_raw = pd.read_excel(arquivo_excel, header=[0, 1])

# Unifica os nomes das colunas: "1° SEMESTRE DE 2019|1° C", etc.
df_raw.columns = [f"{a}|{b}" for a, b in df_raw.columns]

# Remove colunas desnecessárias, como Total
df_raw = df_raw.drop(columns=[col for col in df_raw.columns if "Total" in col])

# Define os nomes exatos das colunas de curso e turno
col_curso = 'CURSO|Unnamed: 0_level_1'
col_turno = 'TURNO|Unnamed: 1_level_1'

# Isola dados fixos
df_fixed = df_raw[[col_curso, col_turno]]
df_fixed.columns = ['curso', 'turno']

# Dados de ciclos
df_data = df_raw.drop(columns=[col_curso, col_turno])

# Corrige ciclos mal formatados, ex: '4°C' → '4° C'
df_data.columns = [col.replace('°C', '° C') for col in df_data.columns]

# Derrete o dataframe (wide → long)
df_melted = df_data.melt(var_name="semestre_ciclo", value_name="quantidade")

# Replica os dados fixos para cada linha derretida
df_melted = pd.concat([pd.concat([df_fixed] * len(df_data.columns), ignore_index=True), df_melted], axis=1)

# Extrai semestre e ano
df_melted[['semestre', 'ano']] = df_melted['semestre_ciclo'].str.extract(r"(\d° SEMESTRE DE) (\d{4})")
df_melted['semestre'] = df_melted['semestre'].str.strip()
df_melted['ano'] = df_melted['ano'].astype(str)

# Extrai ciclo
df_melted['ciclo'] = df_melted['semestre_ciclo'].str.extract(r"\|\s*(\d° C)")

# Gera tabela final no formato template
df_final = df_melted.pivot_table(
    index=['curso', 'turno', 'semestre', 'ano'],
    columns='ciclo',
    values='quantidade',
    aggfunc='first'
).reset_index()

# Garante que todos os ciclos existam como colunas
ciclos_template = ['1° C', '2° C', '3° C', '4° C', '5° C', '6° C']
for ciclo in ciclos_template:
    if ciclo not in df_final.columns:
        df_final[ciclo] = None

# Reorganiza colunas
df_final = df_final[['curso', 'turno', 'semestre', 'ano'] + ciclos_template]

# Salva em CSV
df_final.to_csv("dados_injetados.csv", index=False)

