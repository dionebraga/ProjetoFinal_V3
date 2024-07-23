from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from faker import Faker
import random
import requests
import os
import time

def setup_driver():
    options = Options()
    # options.add_argument("--headless")  # Opcional: executar em modo headless
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    return driver

def login(driver, email, senha):
    url = "http://projetofinal.jogajuntoinstituto.org/"
    driver.get(url)

    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    email_input.send_keys(email)

    senha_input = driver.find_element(By.NAME, "password")
    senha_input.send_keys(senha)

    iniciar_sessao_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Iniciar sessão')]"))
    )
    iniciar_sessao_button.click()
    print("Senha preenchida e botão de login clicado.")

def baixar_imagem_aleatoria():
    url_imagem = "https://picsum.photos/200"
    resposta = requests.get(url_imagem)
    caminho_imagem = os.path.join(os.getcwd(), "imagem_aleatoria.jpg")
    with open(caminho_imagem, 'wb') as file:
        file.write(resposta.content)
    if os.path.exists(caminho_imagem):
        print("Imagem baixada com sucesso.")
        return caminho_imagem
    else:
        raise FileNotFoundError("A imagem não pôde ser baixada.")

def adicionar_produto(driver, nome_produto, descricao_produto, preco_produto, imagem_path):
    adicionar_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Adicionar')]"))
    )
    adicionar_button.click()
    print("Botão 'Adicionar' clicado.")

    nome_produto_input = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.NAME, "name"))
    )
    nome_produto_input.send_keys(nome_produto)
    print(f"Nome do produto ({nome_produto}) preenchido.")

    descricao_produto_input = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.NAME, "description"))
    )
    descricao_produto_input.send_keys(descricao_produto)
    print(f"Descrição do produto ({descricao_produto}) preenchida.")

    categoria_label = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//label[span[text()='Roupas']]"))
    )
    categoria_label.click()
    print("Opção 'Roupas' selecionada.")

    preco_input = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.NAME, "price"))
    )
    preco_input.send_keys(preco_produto)
    print(f"Preço do produto ({preco_produto}) preenchido.")

    imagem_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "image"))
    )
    imagem_input.send_keys(imagem_path)
    print("Imagem do produto enviada.")

    frete_input = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.NAME, "shipment"))
    )
    frete_input.send_keys("Frete grátis")
    print("Frete preenchido.")

    submit_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'ENVIAR NOVO PRODUTO')]"))
    )
    submit_button.click()
    print("Produto adicionado com sucesso.")

    # Esperar a lista de produtos ser atualizada
    time.sleep(5)  # Ajuste o tempo de espera conforme necessário

def listar_produtos(driver):
    try:
        # Localizar a div que contém a lista de produtos
        produtos_div = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'first') and contains(., 'Produtos')]"))
        )

        # Localizar todos os elementos de produto dentro da div
        produtos = produtos_div.find_elements(By.XPATH, ".//following-sibling::div[@class='sc-eEieub jWuGiS']//div[@class='sc-kkGfuU hbqHry']")
        
        lista_produtos = []
        for produto in produtos:
            nome = produto.find_element(By.XPATH, ".//h1").text
            descricao = produto.find_element(By.XPATH, ".//span[1]").text
            preco = produto.find_element(By.XPATH, ".//span[contains(@class, 'price')]").text
            lista_produtos.append({'nome': nome, 'descricao': descricao, 'preco': preco})
            print(f"Produto listado: Nome - {nome}, Descrição - {descricao}, Preço - {preco}")
        return lista_produtos
    except TimeoutException:
        print("Tempo limite excedido ao listar os produtos.")
    except NoSuchElementException as e:
        print("Elemento não encontrado durante a listagem dos produtos:", e)
    except WebDriverException as e:
        print("Erro do WebDriver ao listar os produtos:", e)

def excluir_produto_por_imagem(driver, url_imagem):
    try:
        # Localizar o produto pela URL da imagem
        imagem_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f"//img[@src='{url_imagem}']"))
        )
        produto_element = imagem_element.find_element(By.XPATH, "./ancestor::div[@class='sc-eDPEul WYngD']/following-sibling::div[@class='sc-eldPxv hbqHry']")
        
        # Localizar o botão de exclusão correspondente
        excluir_button = produto_element.find_element(By.XPATH, ".//button[contains(text(), 'Excluir')]")
        excluir_button.click()

        # Confirmar a exclusão se necessário
        confirmar_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirmar')]"))
        )
        confirmar_button.click()
        print(f"Produto com a imagem '{url_imagem}' excluído com sucesso.")

    except TimeoutException:
        print("Tempo limite excedido ao tentar excluir o produto.")
    except NoSuchElementException:
        print(f"Produto com a imagem '{url_imagem}' não encontrado para exclusão.")
    except WebDriverException as e:
        print("Erro do WebDriver ao excluir o produto:", e)

def main():
    driver = setup_driver()
    fake = Faker('pt_BR')

    try:
        email = "dionebraga.work@gmail.com"
        senha = "123456"
        login(driver, email, senha)

        nome_produto = fake.word().capitalize()
        descricao_produto = fake.sentence(nb_words=6)
        preco_produto = f"R$ {random.uniform(10, 100):.2f}".replace('.', ',')
        imagem_path = baixar_imagem_aleatoria()

        adicionar_produto(driver, nome_produto, descricao_produto, preco_produto, imagem_path)

        # Listar produtos
        print("Listando produtos adicionados:")
        listar_produtos(driver)

        # Excluir o produto pelo elemento <img>
        url_imagem = "https://apipf.jogajuntoinstituto.org/1721356468409-457602595.jpg"
        excluir_produto_por_imagem(driver, url_imagem)

        # Listar produtos novamente após exclusão
        print("Listando produtos após exclusão:")
        listar_produtos(driver)

    except TimeoutException as e:
        print("Tempo limite excedido ao esperar por um elemento:", e)
    except NoSuchElementException as e:
        print("Elemento não encontrado:", e)
    except WebDriverException as e:
        print("Erro do WebDriver:", e)
    except Exception as e:
        print(f"Erro durante a execução do script: {e}")
    finally:
        try:
            driver.quit()
        except WebDriverException:
            print("Erro ao fechar o WebDriver.")
        # Remover a imagem baixada
        if 'imagem_path' in locals() and os.path.exists(imagem_path):
            os.remove(imagem_path)

if __name__ == "__main__":
    main()
