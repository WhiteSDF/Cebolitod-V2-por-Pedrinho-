from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class LoginData(BaseModel):
    ra: str
    senha: str

@app.post("/fazer-tarefas")
async def fazer_tarefas(data: LoginData):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://saladofuturo.educacao.sp.gov.br/")

        # Quebrando RA e UF
        ra_completo = data.ra.strip().lower()
        ra = ra_completo[:-2]
        digito = ra_completo[-2:-1]
        uf = ra_completo[-2:].upper()

        # Preencher login
        driver.find_element(By.NAME, "ra").send_keys(ra)
        driver.find_element(By.NAME, "digitoRa").send_keys(digito)
        driver.find_element(By.NAME, "uf").send_keys(uf)
        driver.find_element(By.NAME, "senha").send_keys(data.senha)

        # Clicar em acessar
        driver.find_element(By.XPATH, "//button[contains(text(), 'Acessar')]").click()
        time.sleep(3)

        if "login" in driver.current_url.lower() or "erro" in driver.page_source.lower():
            driver.quit()
            return { "status": "erro" }

        # Acessar página de tarefas SP
        driver.get("https://saladofuturo.educacao.sp.gov.br/tarefasSP")
        time.sleep(2)

        tarefas = driver.find_elements(By.CLASS_NAME, "card-tarefa")
        if not tarefas:
            driver.quit()
            return { "status": "sem_tarefas" }

        nomes_tarefas = []

        for tarefa in tarefas:
            try:
                nome = tarefa.text.split("\n")[0]
                nomes_tarefas.append(nome)
                tarefa.click()
                time.sleep(2)
                botao = driver.find_element(By.XPATH, "//button[contains(text(),'Concluir')]")
                botao.click()
                time.sleep(2)
                driver.back()
                time.sleep(2)
            except:
                continue

        driver.quit()
        return { "status": "ok", "feitas": nomes_tarefas }

    except Exception as e:
        print("Erro:", e)
        return { "status": "erro" }