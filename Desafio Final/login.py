import requests
import json
from faker import Faker

fake = Faker('pt_BR')

# URL da API de login
login_url = 'https://projetofinal.jogajuntoinstituto.org'

# Dados para login
login_data = {
    'email': 'dionebraga.work@gmail.com',
    'password': '123456'
}

# Fazendo a solicitação POST para login
response = requests.post(login_url, data=login_data)

# Verificando a resposta de login
if response.status_code == 200:
    print('Login realizado com sucesso!')

# Salvando a resposta JSON em um arquivo
    with open('login_response.json', 'w') as json_file:
        json.dump(response.json(), json_file, indent=4)
    print('Resposta JSON salva em login_response.json')
else:
    print(f'Falha ao fazer login. Status code: {response.status_code}')
    print('Mensagem de erro:', response.json())
