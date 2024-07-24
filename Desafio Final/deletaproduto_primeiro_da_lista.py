import requests
import json

# URL base da API
base_url = 'https://apipf.jogajuntoinstituto.org'

# Endpoint para login
login_url = f'{base_url}/login'

# Dados de login
login_data = {
    "email": "dionebraga.work@gmail.com",
    "password": "123456"
}

def realizar_login():
    try:
        # Realizar a requisição POST para login e obter o token
        login_response = requests.post(login_url, json=login_data)

        # Verificar se o login foi bem-sucedido
        if login_response.status_code == 200:
            # Extrair o token da resposta
            token = login_response.json().get('token')
            print(f"Token obtido: {token}")
            
            # Salvar o token em um JSON
            with open('token.json', 'w') as token_file:
                json.dump({"token": token}, token_file)
            return token
        else:
            print(f"Falha no login. Status code: {login_response.status_code}")
            print(f"Resposta: {login_response.text}")
            return None
    except Exception as e:
        print(f"Erro ao realizar login: {e}")
        return None

def obter_lista_produtos(token):
    try:
        # Endpoint para obter a lista de produtos
        get_products_url = f'{base_url}'

        # Headers de autenticação com o token obtido
        headers = {
            'Authorization': f'Bearer {token}'
        }

        # Realizar a requisição GET para obter a lista de produtos
        response = requests.get(get_products_url, headers=headers)
        
        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200:
            produtos = response.json()
            print("Lista de produtos:", produtos)
            return produtos
        else:
            print(f"Falha ao obter a lista de produtos. Status code: {response.status_code}")
            print(f"Resposta: {response.text}")
            return None
    except Exception as e:
        print(f"Erro ao obter a lista de produtos: {e}")
        return None

def excluir_produto(token, produto_id):
    try:
        # Endpoint para excluir o produto
        delete_product_url = f'{base_url}/{produto_id}'

        # Headers de autenticação com o token obtido
        headers = {
            'Authorization': f'Bearer {token}'
        }

        # Realizar a requisição DELETE para excluir o produto
        delete_response = requests.delete(delete_product_url, headers=headers)
        
        if delete_response.status_code == 204:
            print(f"Produto com ID {produto_id} foi excluído com sucesso.")
        else:
            print(f"Falha ao excluir o produto com ID {produto_id}. Status code: {delete_response.status_code}")
            print(f"Resposta: {delete_response.text}")
    except Exception as e:
        print(f"Erro ao excluir o produto: {e}")

def main():
    # Realizar login e obter o token
    token = realizar_login()
    
    if token:
        # Obter a lista de produtos
        produtos = obter_lista_produtos(token)
        
        if produtos:
            # Organizar a lista de produtos (por exemplo, por name)
            produtos_organizados = sorted(produtos, key=lambda x: x['name'])
            for produto in produtos_organizados:
                print(f"ID: {produto['idprodutos']}, Nome: {produto['name']}, Preço: {produto['price']}, Categoria: {produto['category']}")

            # Solicitar ao usuário o ID do produto a ser excluído
            produto_id = input("Digite o ID do produto que deseja excluir: ")

            # Excluir o produto especificado pelo usuário
            excluir_produto(token, produto_id)
        else:
            print("Falha ao obter ou processar a lista de produtos.")
    else:
        print("Falha no login, não foi possível continuar.")

if __name__ == "__main__":
    main()
