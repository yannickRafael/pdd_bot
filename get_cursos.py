import requests
from bs4 import BeautifulSoup
import pandas as pd
from config import Config
from utils import save_to_excel

app_config = Config()   

def fetch_courses():
    response = requests.get(app_config.SITE_MAP_URL)
    if response.status_code != 200:
        raise Exception(f"Falha ao acessar a página: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="degreeTable")
    rows = table.find_all("tr")

    courses = []

    for row in rows:
        first_td = row.find("td")
        if not first_td:
            continue

        anchor = first_td.find("a")
        if not anchor:
            continue

        full_text = anchor.get_text(strip=True)
        href = anchor.get("href")
        full_link = app_config.BASE_URL + href if href.startswith("/") else href

        # Tenta extrair o nome e código do curso
        if "(" in full_text and ")" in full_text:
            try:
                name = full_text.rsplit("(", 1)[0].strip()
                code = full_text.rsplit("(", 1)[1].replace(")", "").strip()
                courses.append({
                    "cu_nome": name,
                    "cu_code": code,
                    "cu_link": full_link
                })
            except Exception as e:
                print(f"Erro ao processar linha: {full_text}. Erro: {e}")
                continue

    return courses


cursos = fetch_courses()
save_to_excel(cursos)
