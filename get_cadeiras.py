import pandas as pd
import requests
from bs4 import BeautifulSoup
import pickle
from config import Config
from login import do_login

# Configuração
app_config = Config()

BASE_DISCIPLINAS_URL = app_config.BASE_DISCIPLINAS_URL
BASE_AVALIACAO_URL = app_config.BASE_AVALIACAO_URL
BASE_DOMAIN = app_config.BASE_DOMAIN
# Link corrigido de performance (domínio final usado pelo estudante)
BASE_PERFORMANCE = app_config.BASE_PERFORMANCE

COOKIES_FILE = app_config.COOKIES_FILE_NAME

# Read cookies and check session
def load_authenticated_session():
    s = requests.Session()
    try:
        with open(COOKIES_FILE, 'rb') as f:
            cookies = pickle.load(f)
            s.cookies.update(cookies)
        test = s.get(app_config.SITE_MAP_URL, timeout=5)
        if "Login" in test.text:
            raise Exception("Expired Session")
    except Exception:
        print("Invalid Session, trying authentication...")
        s = do_login()
        with open(COOKIES_FILE, 'wb') as f:
            pickle.dump(s.cookies, f)
    return s

# Get subjects from website
def fetch_disciplinas():
    session = load_authenticated_session()
    cursos_df = pd.read_excel(app_config.COURSES_FILE_NAME)
    disciplinas = []

    for _, row in cursos_df.iterrows():
        cu_code = row["cu_code"]
        cu_link = BASE_DISCIPLINAS_URL.format(cu_code.lower())

        try:
            response = session.get(cu_link, timeout=10)
            if response.status_code != 200:
                print(f"[Erro] Falha ao acessar {cu_link}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.select("table a[href*='/disciplinas/']")

            for a in links:
                ca_nome = a.get_text(strip=True)
                ca_link = a.get("href")
                if not ca_nome or not ca_link:
                    continue

                ca_code = ca_link.split("/disciplinas/")[1].split("/")[0]
                full_ca_link = ca_link if ca_link.startswith("http") else BASE_DOMAIN + ca_link

                # Buscar link de rendimento académico
                avaliacao_url = BASE_AVALIACAO_URL.format(ca_code)
                perf_link = ""
                try:
                    perf_res = session.get(avaliacao_url, timeout=10)
                    if perf_res.status_code == 200:
                        perf_soup = BeautifulSoup(perf_res.text, "html.parser")
                        perf_anchor = perf_soup.find("a", href=True, string="Rendimento académico")
                        if perf_anchor:
                            perf_href = perf_anchor["href"]
                            if "executionCourseID=" in perf_href:
                                execution_id = perf_href.split("executionCourseID=")[-1]
                                perf_link = BASE_PERFORMANCE.format(execution_id)
                    else:
                        print(f"  [!] Avaliação indisponível para {ca_code}")
                except Exception as e:
                    print(f"  [x] Erro ao acessar avaliação de {ca_code}: {e}")
                    perf_link = ""

                disciplinas.append({
                    "ca_nome": ca_nome,
                    "ca_code": ca_code,
                    "ca_link": full_ca_link,
                    "ca_cucode": cu_code,
                    "ca_performance": perf_link
                })

            print(f"[OK] {cu_code} - {len(links)} disciplinas processadas.")

        except Exception as e:
            print(f"[Erro] {cu_code} - {e}")

    # Salva em Excel
    df = pd.DataFrame(disciplinas)
    df.to_excel(app_config.SUBJECTS_FILE_NAME, index=False)
    print("Ficheiro 'cadeiras.xlsx' salvo com sucesso.")

if __name__ == "__main__":
    fetch_disciplinas()
