import pandas as pd
from config import Config
import random
from service.curso_service import Curso_Service

app_config = Config()

def store_courses_on_db():
    # Load the Excel file
    df = pd.read_excel(app_config.COURSES_FILE_NAME)
    print("Colunas do DataFrame:", df.columns.tolist())
    # Generate cu_id with cu_code + random suffix
    def store_and_retrieve(row):
        print(f"Processing row: {row}")
        cu_code = row["cu_code"]
        cu_nome = row["cu_nome"]
        res = Curso_Service.create_curso(str(cu_nome), str(cu_code), 0)
        if res and bool(res.get("success")):
            return res["data"]["cu_id"]
        else:
            return "failed"

    # Add or update cu_id column
    df["cu_id"] = df.apply(store_and_retrieve, axis=1)

    # Save back to the same Excel file
    df.to_excel(app_config.COURSES_FILE_NAME, index=False)

    print("cu_id column added or updated with cu_code-based random IDs.")

