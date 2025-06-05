import pandas as pd
from config import Config
import random
from service.curso_service import Curso_Service
from service.cadeira_service import Cadeira_Service
from service.avaliacao_service import Avaliacao_Service

app_config = Config()

def store_and_retrieve_curso(row):
        cu_code = row["cu_code"]
        cu_nome = row["cu_nome"]
        res = Curso_Service.create_curso(str(cu_nome), str(cu_code), 0)
        if res and bool(res.get("success")):
            return res["data"]["cu_id"]
        else:
            return "failed"
        
def store_and_retrieve_cadeira(row):
        ca_code = row["ca_code"]
        ca_nome = row["ca_nome"]
        ca_cuid = row["ca_cuid"]
        ca_link = row["ca_link"]
        res = Cadeira_Service.create_cadeira(str(ca_nome), str(ca_code), ca_cuid, ca_link, 0)
        print('DEBUG: Cadeira Service Response:', res)
        if res and bool(res.get("success")):
            return res["data"]["ca_id"]
        else:
            return "failed"
def store_and_retrieve_avaliacao(row):
    a_nome = row['a_nome']
    a_code = row['a_code']
    a_caid = row['a_caid']
    a_nota_max = row['nota_max']
    
    res = Avaliacao_Service.create_avaliacao(
        str(a_nome),
        str(a_code),
        a_caid,
        a_nota_max,
        0 )
    
    print('DEBUG: Avaliacao Service Response:', res)
    if res and bool(res.get("success")):
        return res["data"]["a_id"]
    else:
        return "failed"


def store_courses_on_db():
    # Load the Excel file
    df = pd.read_excel(app_config.COURSES_FILE_NAME)

    # Add or update cu_id column
    df["cu_id"] = df.apply(store_and_retrieve_curso, axis=1)

    # Save back to the same Excel file
    df.to_excel(app_config.COURSES_FILE_NAME, index=False)


def store_cadeiras_on_db():
    # Carrega cursos e mapeia cu_code -> cu_id
    df_cursos = pd.read_excel(app_config.COURSES_FILE_NAME)
    curso_map = dict(zip(df_cursos["cu_code"], df_cursos["cu_id"]))

    # Carrega cadeiras
    df = pd.read_excel(app_config.SUBJECTS_FILE_NAME)

    # Preenche nova coluna ca_cuid com base em ca_cucode (usando o dicionário de cursos)
    df["ca_cuid"] = df["ca_cucode"].map(curso_map)

    # Aplica a criação da cadeira
    df["ca_id"] = df.apply(store_and_retrieve_cadeira, axis=1)

    # Salva de volta
    df.to_excel(app_config.SUBJECTS_FILE_NAME, index=False)

def store_avaliacoes_on_db():
    # Carrega os ficheiros
    df_avaliacao = pd.read_excel(app_config.AVALIACAO_FILE_NAME)
    df_cadeiras = pd.read_excel(app_config.SUBJECTS_FILE_NAME)

    # Cria um dicionário {ca_code: ca_id}
    code_to_id = dict(zip(df_cadeiras["ca_code"], df_cadeiras["ca_id"]))

    # Preenche a nova coluna com base no ca_code
    df_avaliacao["a_caid"] = df_avaliacao["ca_code"].map(code_to_id)

    # Aplica a função de inserção
    df_avaliacao["a_id"] = df_avaliacao.apply(store_and_retrieve_avaliacao, axis=1)

    # Salva de volta o ficheiro correto
    df_avaliacao.to_excel(app_config.AVALIACAO_FILE_NAME, index=False)




# store_courses_on_db()
# store_cadeiras_on_db()
store_avaliacoes_on_db()
