import re
from config import Config
import pandas as pd
app_config = Config()


def extract_hidden_lt(text):
    pattern = r'<input type="hidden" name="lt" value="(.*?)" />'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None

def extract_hidden_execution(text):
    pattern = r'<input type="hidden" name="execution" value="(.*?)" />'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None
    
def extract_jsessionid(cookies):
    for c in cookies:
        if c.name.lower().startswith("jsessionid"):
            return c.value
    raise Exception("JSESSIONID não encontrado nos cookies.")

def save_to_excel(courses, filename=app_config.COURSES_FILE_NAME):
    df = pd.DataFrame(courses)
    df.to_excel('files/'+filename, index=False)
    print(f"Arquivo Excel salvo com sucesso como '{filename}'")