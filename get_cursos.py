import requests
from bs4 import BeautifulSoup
import pandas as pd
from config import Config
from utils import save_to_excel

app_config = Config()   

# Function to get courses from the website
def fetch_courses():

    # Get the site map page
    response = requests.get(app_config.SITE_MAP_URL)
    if response.status_code != 200:
        raise Exception(f"Falha ao acessar a página: {response.status_code}")

    # Analyze the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="degreeTable")

    #Get all table rows
    rows = table.find_all("tr")

    #list of courses
    courses = []

    #Iterate through each row
    for row in rows:
        first_td = row.find("td")
        if not first_td:
            continue

        # Check if the first <td> contains an <a> tag
        anchor = first_td.find("a")
        if not anchor:
            continue


        # Extract the full text and link from the <a> tag
        full_text = anchor.get_text(strip=True)
        href = anchor.get("href")
        full_link = app_config.BASE_URL + href if href.startswith("/") else href

        # Separate and Extract course name and code
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
                print(f"Error processing row: {full_text}. Erro: {e}")
                continue

    return courses


cursos = fetch_courses()
save_to_excel(cursos)
