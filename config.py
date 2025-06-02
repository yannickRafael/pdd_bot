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
    