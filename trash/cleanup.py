import pandas as pd
import re

def transformar_desistentes(caminho_csv):
    # Ler o CSV ignorando as duas primeiras linhas de cabeçalho
    df = pd.read_csv(caminho_csv, skiprows=2, header=None, dtype=str)
    
    # Ler os cabeçalhos originais para criar colunas estruturadas
    with open(caminho_csv, 'r', encoding='utf-8') as f:
        semestres = f.readline().strip().split(',')
        ciclos = f.readline().strip().split(',')

    # Criar cabeçalhos combinados
    novos_cabecalhos = []
    current_semestre = ''
    for s, c in zip(semestres, ciclos):
        if s:
            current_semestre = s
        header = f"{current_semestre} | {c}" if c else current_semestre
        novos_cabecalhos.append(header.strip())

    # Ajustar cabeçalhos para combinar com o número de colunas
    df.columns = novos_cabecalhos[:len(df.columns)]
    
    # Remover coluna Total se existir
    df = df.drop(columns=[col for col in df.columns if 'Total' in col], errors='ignore')

    # Derreter o dataframe para formato longo
    id_vars = ['CURSO', 'TURNO']
    df_melted = df.melt(
        id_vars=id_vars,
        var_name='semestre_ciclo', 
        value_name='valor'
    ).dropna()

    # Extrair ano e semestre usando regex
    pattern = r".*(\d+)° SEMESTRE DE (\d{4}).*\| (\d+° C)"
    extracted = df_melted['semestre_ciclo'].str.extract(pattern)
    
    # Combinar os dados extraídos
    df_clean = pd.concat([
        df_melted.drop(columns=['semestre_ciclo']),
        extracted.rename(columns={
            0: 'semestre',
            1: 'ano',
            2: 'ciclo'
        })
    ], axis=1)

    # Converter tipos de dados e limpar valores
    df_clean = df_clean.dropna(subset=['semestre', 'ano', 'ciclo'])
    df_clean['semestre'] = df_clean['semestre'].astype(int)
    df_clean['ano'] = df_clean['ano'].astype(int)
    df_clean['valor'] = pd.to_numeric(df_clean['valor'], errors='coerce').fillna(0.0)

    # Pivotar para formato final
    df_final = df_clean.pivot_table(
        index=['CURSO', 'TURNO', 'ano', 'semestre'],
        columns='ciclo',
        values='valor',
        aggfunc='first'
    ).reset_index()

    # Renomear e ordenar colunas
    df_final.columns.name = None
    df_final = df_final.rename(columns={
        'CURSO': 'curso',
        'TURNO': 'turno'
    })
    
    # Garantir todas as colunas de ciclo
    for ciclo in [f'{i}° C' for i in range(1,7)]:
        if ciclo not in df_final.columns:
            df_final[ciclo] = 0.0

    col_order = ['curso', 'turno', 'semestre', 'ano'] + [f'{n}° C' for n in range(1,7)]
    return df_final[col_order].sort_values(by=['curso', 'turno', 'ano', 'semestre'])

# Uso:
df_transformado = transformar_desistentes('dados_original.csv')
df_transformado.to_csv('dados_transformados.csv', index=False, float_format='%.1f')