import requests
import json
import csv

# URL da API para criar usuário
create_user_url = 'https://desafiopython.jogajuntoinstituto.org/api/users/'

# Dados para criação de usuário 
user_data = {
     'username': 'dionesilhabelatechijj',
        'email': 'dionesilhabelatechijj@gmail.com',
        'password': 'Ilhabela_tech',
        'phone': '12982912522',
        'address': 'Rua da Ietec, Ilhabela-SP, Brasil',
        'cpf': '123.456.789-01'
}

# Função para criar um usuário
def create_user():
    try:
        # Fazendo a solicitação POST para criar o usuário
        response = requests.post(create_user_url, json=user_data)
        response.raise_for_status() 
                
        if response.status_code == 201:
            print(f'Usuário {user_data["username"]} criado com sucesso!')
        else:
            print(f'Falha ao criar usuário {user_data["username"]}. Status code: {response.status_code}')
            print('Mensagem de erro:', response.json())
    except requests.exceptions.RequestException as e:
        print(f'Erro ao criar usuário {user_data["username"]}:', e)

    return user_data['email'], user_data['password']

# Função para fazer login
def login(email, password):
    login_url = 'https://desafiopython.jogajuntoinstituto.org/api/users/login/'
    login_data = {
        'email': email,
        'password': password
    }

    try:
        # Fazendo a solicitação POST para login
        response = requests.post(login_url, json=login_data)
        response.raise_for_status()
        
        if response.status_code == 200:
            print('Login realizado com sucesso!')
            login_response = response.json()
            
            # Ordenando os dados por chave (ordem alfabética)
            sorted_login_response = dict(sorted(login_response.items()))
    
            # Salvando a resposta JSON em um arquivo
            # ident=4 especifica que o JSON deve ser formatado com recuo de 4 espaços para facilitar a leitura.
            # login_response.json', 'w', Abre o arquivo login_response.json em modo de escrita ('w'). With garante que o arquivo seja fechado corretamente após seu uso mesmo com execções
            # A variável sorted_login_response armazena os dados JSON de uma resposta HTTP organizados por chave, facilitando o processamento e apresentação ordenada desses dados.
            
            with open('login_response.json', 'w') as json_file:
                json.dump(sorted_login_response, json_file, indent=4)
            print('Resposta JSON salva em login_response.json')
            
            # Salvando a resposta JSON em um arquivo CSV
            # csv_writer é um objeto que simplifica a escrita de dados em arquivos CSV, permitindo uma organização estruturada por linhas e colunas, adequando os dados conforme necessário.
            with open('login_response.csv', 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                
                # Escrevendo o cabeçalho
                # Obter as chaves do dicionário sorted_login_response e escrevê-las como o cabeçalho de um arquivo CSV utilizando o objeto csv_writer.
                header = sorted_login_response.keys()
                csv_writer.writerow(header)
                
                # Escrevendo os dados
                # Escreve valores contidos no dicionário sorted_login_response como uma linha no arquivo CSV utilizando o csv_writer, para cpmpletar o processo de salvar os dados e estruturar o cod.
                csv_writer.writerow(sorted_login_response.values())
                
            # indica que a resposta foi salva com sucesso
            print('Resposta JSON salva em login_response.csv')

            # Exibindo os dados ordenados
            for key, value in sorted_login_response.items():
                print(f'{key}: {value}')
        else:
            print(f'Falha ao fazer login. Status code: {response.status_code}')
            print('Mensagem de erro:', response.json())
    except requests.exceptions.RequestException as e:
        print('Erro ao fazer login:', e)
        return None

# Função para obter a listagem de usuários criadas no sistema, indicando a url específica
def get_users_list():
    list_users_url = 'https://desafiopython.jogajuntoinstituto.org/api/users/'

    try:
        # Fazendo a solicitação GET para obter a listagem de usuários
        response = requests.get(list_users_url)
        response.raise_for_status()
        
        if response.status_code == 200:
            print('Listagem de usuários obtida com sucesso!')
            users_list = response.json()
            
            # Ordenando a listagem de usuários por nome de usuário
            # lambda x: x['username'] cria uma função anônima que serve como critério de ordenação, especificamente para ordenar uma lista de usuários pelo campo 'username'.
            sorted_users_list = sorted(users_list, key=lambda x: x['username'])
            
            # Salvando a listagem de usuários em um arquivo JSON
            with open('users_list.json', 'w') as json_file:
                json.dump(sorted_users_list, json_file, indent=4)
            print('Listagem de usuários salva em users_list.json')
            
            # Salvando a listagem de usuários em um arquivo CSV
            with open('users_list.csv', 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                
                # Escrevendo o cabeçalho
                if sorted_users_list:
                    header = sorted_users_list[0].keys()
                    csv_writer.writerow(header)
                    
                    # Escrevendo os dados
                    for user in sorted_users_list:
                        csv_writer.writerow(user.values())
                        
            print('Listagem de usuários salva em users_list.csv')

            # Exibindo a listagem de usuários ordenada
            for user in sorted_users_list:
                print(f"Username: {user['username']}, 
                        Email: {user['email']}, 
                        Phone: {user['phone']}, 
                        Address: {user['address']}, 
                        CPF: {user['cpf']}")
        else:
            print(f'Falha ao obter a listagem de usuários. Status code: {response.status_code}')
            print('Mensagem de erro:', response.json())
    except requests.exceptions.RequestException as e:
        print('Erro ao obter a listagem de usuários:', e)

# Criando um usuário
email, password = create_user()

# Fazendo login com o usuário criado
login(email, password)

# Obtendo a listagem de usuários
get_users_list()
