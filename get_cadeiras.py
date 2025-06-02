import pandas as pd
import requests
from bs4 import BeautifulSoup
from config import Config

app_config = Config()

# Base URL para acessar as páginas de disciplinas
BASE_PAGE_URL = "https://fenixlbg.isutc.ac.mz:9443/isutc/cursos/{}/paginas-de-disciplinas"
BASE_DOMAIN = "https://fenixlbg.isutc.ac.mz:9443"

# Lê os cursos do arquivo Excel
cursos_df = pd.read_excel(app_config.COURSES_FILE_NAME)

disciplinas = []

# Para cada curso no Excel
for _, row in cursos_df.iterrows():
    cu_code = row["cu_code"]
    cu_link = BASE_PAGE_URL.format(cu_code.lower())

    try:
        response = requests.get(cu_link, timeout=10)
        if response.status_code != 200:
            print(f"[Erro] Falha ao acessar {cu_link}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Procura todos os links para disciplinas
        links = soup.select("table a[href*='/disciplinas/']")

        for a in links:
            ca_nome = a.get_text(strip=True)
            ca_link = a.get("href")
            if not ca_nome or not ca_link:
                continue

            # Extrair o código da cadeira da URL
            ca_code = ca_link.split("/disciplinas/")[1].split("/")[0]

            disciplinas.append({
                "ca_nome": ca_nome,
                "ca_code": ca_code,
                "ca_link": ca_link if ca_link.startswith("http") else BASE_DOMAIN + ca_link,
                "ca_cucode": cu_code
            })

        print(f"[OK] {cu_code} - {len(links)} disciplinas encontradas.")

    except Exception as e:
        print(f"[Erro] {cu_code}: {e}")

# Salvar os dados em um ficheiro Excel
df = pd.DataFrame(disciplinas)
df.to_excel("cadeiras.xlsx", index=False)
