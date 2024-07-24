import requests
import json

# URL da API de login
url = "https://apipf.jogajuntoinstituto.org/login"#'https://desafiopython.jogajuntoinstituto.org/api/users/login/'

# Dados para login
register_data = {
    'email': 'dionebraga.work@gmail.com',
    'password': '123456'
}

# Fazendo a solicitação POST para login
response = requests.post(url, json=register_data)

# Verificando a resposta de login
if response.status_code == 201:
    print('Login realizado com sucesso!')
    # Salvando a resposta JSON em um arquivo
    with open('login_response.json', 'w') as json_file:
        json.dump(response.json(), json_file, indent=4)
    print('Resposta JSON salva em login_response.json')
else:
    print(f'Falha ao fazer login. Status code: {response.status_code}')
    print('Status do usuário:', response.json())
