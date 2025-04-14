import pandas as pd

def generate_basic_insights(df: pd.DataFrame) -> str:
    summary = df.describe(include='all').to_string()
    info = f"O conjunto de dados tem {df.shape[0]} linhas e {df.shape[1]} colunas.\n\nResumo estatístico:\n{summary}"
    return info
