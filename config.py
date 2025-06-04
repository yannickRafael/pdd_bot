import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    FENIX_PASSWORD = os.getenv('FENIX_PASSWORD')
    FENIX_USERNAME = os.getenv('FENIX_USERNAME')
    FENIX_URL = os.getenv('FENIX_URL')
    FENIX_LOGIN_URL = os.getenv('FENIX_LOGIN_URL')
    SUCCESS_LOGIN_STATUS = int(os.getenv('SUCCESS_LOGIN_STATUS', 200))
    FENIX_PROTECTED_URL = os.getenv('FENIX_PROTECTED_URL')
    SITE_MAP_URL = os.getenv('SITE_MAP_URL')
    BASE_URL = os.getenv('BASE_URL')
    COURSES_FILE_NAME= os.getenv('COURSES_FILE_NAME')
    SUBJECTS_FILE_NAME= os.getenv('SUBJECTS_FILE_NAME')
    COOKIES_FILE_NAME= os.getenv('COOKIES_FILE_NAME')
    AVALIACAO_FILE_NAME = os.getenv('AVALIACAO_FILE_NAME')
    PERFORMANCE_FILE_NAME = os.getenv('PERFORMANCE_FILE_NAME')
    STUDENTS_FILE_NAME = os.getenv('STUDENTS_FILE_NAME')
    DEBUG = os.environ.get('DEBUG') == 'True'
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')

    A_CODE_NOMES = {
    "TPC1": "Trabalho Para Casa 1",
    "TPC2": "Trabalho Para Casa 2",
    "MT1": "Mini-Teste 1",
    "MT2": "Mini-Teste 2",
    "T1": "Teste 1",
    "T2": "Teste 2",
    "TI1": "Teste Intermédio 1",
    "TG1": "Trabalho de Grupo 1",
    "TG2": "Trabalho de Grupo 2",
    "TL1": "Trabalho Laboratorial 1",
    "TP1": "Trabalho Prático 1",
    "EX1": "Exame 1",
    "EX2": "Exame 2",
}
    