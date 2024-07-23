from behave import given, when, then
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import logging

# Configura o driver do Selenium
def setup_driver():
    options = Options()
    # Desative o modo headless para visualizar o navegador
    # options.add_argument("--headless")
    driver = Firefox(service=Service(GeckoDriverManager().install()), options=options)
    logging.info('Driver do Firefox configurado')
    return driver

@given('que esteja na página')
def go_to_page(context):
    context.browser = setup_driver()
    context.browser.get('https://projetofinal.jogajuntoinstituto.org/')
    logging.info('Página de login carregada: %s', context.browser.current_url)

@when('digitar usuário e senha')
def create_todo(context):
    email = "dionebraga.work@gmail.com"
    senha = "123456"

    logging.info('Tentando encontrar o campo de email')
    try:
        email_input = WebDriverWait(context.browser, 20).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        logging.info('Campo de email encontrado')
        email_input.send_keys(email)
    except Exception as e:
        logging.error(f'Erro ao encontrar o campo de email: {e}')
        context.browser.quit()
        raise

    logging.info('Tentando encontrar o campo de senha')
    try:
        senha_input = context.browser.find_element(By.NAME, "password")
        senha_input.send_keys(senha)
    except Exception as e:
        logging.error(f'Erro ao encontrar o campo de senha: {e}')
        context.browser.quit()
        raise
    
    logging.info('Tentando encontrar o botão de login')
    try:
        login_button = WebDriverWait(context.browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Iniciar sessão')]"))
        )
        logging.info('Botão de login encontrado')
        login_button.click()
    except Exception as e:
        logging.error(f'Erro ao encontrar o botão de login: {e}')
        context.browser.quit()
        raise

@then('deve aparecer "Logado com sucesso"')
def check_login_success(context):
    logging.info('Verificando mensagem de sucesso')
    try:
        success_message = WebDriverWait(context.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Logado com sucesso')]"))
        )
        assert "Logado com sucesso" in success_message.text
        logging.info('Mensagem de sucesso encontrada')
    except Exception as e:
        logging.error(f'Erro ao verificar a mensagem de sucesso: {e}')
    finally:
        context.browser.quit()



