import pandas as pd
from pathlib import Path

# Ficheiros de entrada e saída
files = {
    "avaliacao": ("avaliacao.xlsx", "clean_avaliacao.xlsx"),
    "cadeiras": ("cadeiras.xlsx", "clean_cadeiras.xlsx"),
    "cursos": ("cursos.xlsx", "clean_cursos.xlsx"),
    "estudantes": ("estudantes.xlsx", "clean_estudantes.xlsx"),
    "performance": ("performance.xlsx", "clean_performance.xlsx"),
}

# Colunas desejadas em cada ficheiro limpo
columns_to_keep = {
    "avaliacao": ["a_nome", "a_code", "nota_max"],
    "cadeiras": ["ca_nome", "ca_code", "ca_link"],
    "cursos": ["cu_nome", "cu_code"],
    "estudantes": ["e_nome", "e_code"],
    "performance": ["nota", "e_code", "a_code"],
}

def clean_and_export_files():
    for key, (input_file, output_file) in files.items():
        path = Path(input_file)
        if path.exists():
            print(f"🧹 Limpando {input_file}...")
            df = pd.read_excel(path)

            # Normaliza nomes de colunas para evitar problemas com maiúsculas ou espaços
            df.columns = [col.strip().lower() for col in df.columns]
            clean_columns = columns_to_keep[key]

            # Renomeia para nomes padronizados
            col_map = {
                col: next((c for c in clean_columns if c.lower() == col), col)
                for col in df.columns
            }
            df.rename(columns=col_map, inplace=True)

            # Seleciona somente as colunas desejadas
            df = df[[c for c in clean_columns if c in df.columns]]

            df.to_excel(output_file, index=False)
            print(f"✅ {output_file} criado com sucesso.")
        else:
            print(f"⚠️ Ficheiro {input_file} não encontrado.")

if __name__ == "__main__":
    clean_and_export_files()
