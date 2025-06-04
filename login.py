import requests
import pickle
import os
from config import Config
from utils import extract_hidden_lt, extract_hidden_execution

app_config = Config()
COOKIE_FILE = app_config.COOKIES_FILE_NAME


def save_cookies(session: requests.Session):
    with open(COOKIE_FILE, "wb") as f:
        pickle.dump(session.cookies, f)


def load_cookies(session: requests.Session):
    with open(COOKIE_FILE, "rb") as f:
        session.cookies.update(pickle.load(f))


def is_session_valid(session: requests.Session) -> bool:
    """Verifica se a sessão está válida tentando acessar uma página protegida"""
    protected_url = app_config.FENIX_PROTECTED_URL
    response = session.get(protected_url)
    return response.status_code == 200 and "logout" in response.text.lower()


def do_login() -> requests.Session:
    session = requests.Session()
    response = session.get(app_config.FENIX_LOGIN_URL)

    lt = extract_hidden_lt(response.text)
    execution = extract_hidden_execution(response.text)

    payload = {
        'username': app_config.FENIX_USERNAME,
        'password': app_config.FENIX_PASSWORD,
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit',
        'submit': 'LOGIN'
    }

    login_response = session.post(app_config.FENIX_LOGIN_URL, data=payload)

    if login_response.status_code != app_config.SUCCESS_LOGIN_STATUS:
        raise Exception("Falha ao realizar login: " + login_response.text)

    print("Login realizado com sucesso.")
    save_cookies(session)
    return session


def load_or_login() -> requests.Session:
    session = requests.Session()

    if os.path.exists(COOKIE_FILE):
        try:
            load_cookies(session)
            if is_session_valid(session):
                print("Sessão restaurada com sucesso.")
                return session
            else:
                print("Cookies expiraram. Realizando novo login...")
        except Exception as e:
            print(f"Erro ao carregar cookies: {e}. Fazendo login novamente...")

    # Se não conseguiu restaurar, faz login
    return do_login()


# Exemplo de uso
session = load_or_login()
