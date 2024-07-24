import requests

# URL base da API
base_url = 'https://apipf.jogajuntoinstituto.org'

# Endpoint para obter a lista de produtos
get_products_url = f'{base_url}'

# Headers de autenticação (adicione os valores corretos)
headers = {
    'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjI0MCwiaWF0IjoxNzIxNzcyNjUxLCJleHAiOjE3MjE4NTkwNTF9.uRMBLzOOazGwVvJoH5m6snbLpmqzRWMmbeQ6TnHf8Hs'
}

# Realizar a requisição GET para obter a lista de produtos
response = requests.get(get_products_url, headers=headers)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    produtos = response.json()
    print("Lista de produtos:", produtos)

    # Vamos assumir que queremos excluir o primeiro produto da lista
    if produtos:
        produto_id = produtos[0]['id']
        delete_product_url = f'{base_url}/{produto_id}'

        # Realizar a requisição DELETE para excluir o produto
        delete_response = requests.delete(delete_product_url, headers=headers)

        if delete_response.status_code == 204:
            print(f"Produto com ID {produto_id} foi excluído com sucesso.")
        else:
            print(f"Falha ao excluir o produto com ID {produto_id}. Status code: {delete_response.status_code}")
    else:
        print("Nenhum produto encontrado na lista.")
else:
    print(f"Falha ao obter a lista de produtos. Status code: {response.status_code}")
