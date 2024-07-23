import requests
import json

# URL da API de login
login_url = 'https://desafiopython.jogajuntoinstituto.org/api/users/login/'

# Dados para login
login_data = {
    'email': 'dionesilhabelatechijj@gmail.com',
    'password': 'Ilhabela_tech'
}

# Fazendo a solicitação POST para login
response = requests.post(login_url, json=login_data)

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
