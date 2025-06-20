import pandas as pd
import requests
from bs4 import BeautifulSoup
import pickle
from login import do_login
from config import Config

app_config = Config()
COOKIES_FILE = app_config.COOKIES_FILE_NAME
A_CODE_NOMES = app_config.A_CODE_NOMES


# Carrega sessão autenticada
def load_authenticated_session():
    s = requests.Session()
    try:
        with open(COOKIES_FILE, 'rb') as f:
            cookies = pickle.load(f)
            s.cookies.update(cookies)
        # Testa validade
        r = s.get(app_config.SITE_MAP_URL, timeout=5)
        if "Login" in r.text:
            raise Exception("Sessão expirada")
    except Exception:
        print("Sessão inválida, autenticando novamente...")
        s = do_login()
        with open(COOKIES_FILE, 'wb') as f:
            pickle.dump(s.cookies, f)
    return s


def extract_performance_data():
    session = load_authenticated_session()

    cadeiras = pd.read_excel(app_config.SUBJECTS_FILE_NAME)  # ca_code, ca_performance

    avaliacoes = []
    estudantes = {}
    desempenho = []

    for _, row in cadeiras.iterrows():
        ca_code = row["ca_code"]
        perf_url = row["ca_performance"]

        print(f"A aceder {ca_code}...")

        try:
            r = session.get(perf_url, timeout=10)
            if r.status_code != 200:
                print(f"Falha ao acessar {perf_url}")
                continue

            soup = BeautifulSoup(r.text, "html.parser")
            tables = soup.select("table.tab_complex")

            for table in tables:
                rows = table.find_all("tr")
                if len(rows) < 2:
                    continue

                # Cabeçalho
                headers = [th.get_text(strip=True) for th in rows[0].find_all("th")]
                a_codes = headers[3:-2]  # Ignora Número, Nome, Assiduidade, Acumulado, Provisória

                # Última linha = nota máxima
                nota_max_row = rows[-1]
                nota_max_values = [td.get_text(strip=True) for td in nota_max_row.find_all("td")][3:-2]

                for a_code, nota_max in zip(a_codes, nota_max_values):
                    a_nome = A_CODE_NOMES.get(a_code.upper(), "Desconhecido")
                    avaliacoes.append({
                        "a_nome": a_nome,
                        "a_code": a_code,
                        "ca_code": ca_code,
                        "nota_max": nota_max
                    })

                # Demais estudantes
                for row in rows[1:-1]:  # Ignora header e nota máxima
                    cols = row.find_all("td")
                    if len(cols) < len(headers):
                        continue

                    e_code = cols[0].get_text(strip=True)
                    e_nome = cols[1].get_text(strip=True)
                    estudantes[e_code] = e_nome

                    for i, a_code in enumerate(a_codes):
                        nota_str = cols[i + 3].get_text(strip=True)
                        if nota_str and nota_str.upper() != "FA":
                            try:
                                nota = float(nota_str)
                                desempenho.append({
                                    "a_code": a_code,
                                    "e_code": e_code,
                                    "nota": nota,
                                    "ca_code": ca_code
                                })
                            except ValueError:
                                pass  # Ignora notas inválidas

            print(f"{ca_code} processado.")

        except Exception as e:
            print(f"Erro ao processar {ca_code}: {e}")

    # Salvar Excel
    pd.DataFrame(avaliacoes).to_excel(app_config.AVALIACAO_FILE_NAME, index=False)
    pd.DataFrame(list(estudantes.items()), columns=["e_code", "e_nome"]).to_excel(app_config.STUDENTS_FILE_NAME, index=False)
    pd.DataFrame(desempenho).to_excel(app_config.PERFORMANCE_FILE_NAME, index=False)
    print("Ficheiros avaliacao.xlsx, estudantes.xlsx e performance.xlsx gerados com sucesso.")


if __name__ == "__main__":
    extract_performance_data()
