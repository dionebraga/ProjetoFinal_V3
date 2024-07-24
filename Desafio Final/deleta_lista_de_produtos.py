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
        
        if delete_response.status_code == 200:
            return True, "Produto deletado com sucesso!"
        else:
            return False, f"Falha ao excluir o produto com ID {produto_id}. Status code: {delete_response.status_code}. Resposta: {delete_response.text}"
    except Exception as e:
        return False, f"Erro ao excluir o produto: {e}"

def exibir_produtos(produtos, titulo):
    print(f"\n========== {titulo} ==========")
    for produto in produtos:
        print(f"ID: {produto['idprodutos']}, Nome: {produto['name']}, Preço: {produto['price']}, Categoria: {produto['category']}")
    print("===================================================")

def main():
    # Realizar login e obter o token
    token = realizar_login()
    
    if token:
        produtos_deletados = []
        produtos = obter_lista_produtos(token)
        
        while produtos:
            # Exibir a lista de produtos disponíveis
            exibir_produtos(produtos, "Lista de Produtos Disponíveis")

            # Solicitar ao usuário o ID do produto a ser excluído
            produto_id = input("Digite o ID do produto que deseja excluir: ")

            # Encontrar o produto na lista para obter o nome
            produto_a_excluir = next((p for p in produtos if p['idprodutos'] == int(produto_id)), None)
            
            if produto_a_excluir:
                # Excluir o produto especificado pelo usuário
                sucesso, mensagem = excluir_produto(token, produto_id)
                
                if sucesso:
                    produto_a_excluir["description"] = "deletado"
                    produtos_deletados.append(produto_a_excluir)
                    print(mensagem)
                    
                    # Atualizar a lista de produtos removendo o produto excluído
                    produtos = [p for p in produtos if p['idprodutos'] != int(produto_id)]

                    # Exibir o histórico de produtos deletados
                    exibir_produtos(produtos_deletados, "Histórico de Produtos Deletados")
                else:
                    print(mensagem)
            else:
                print("Produto não encontrado. Verifique o ID e tente novamente.")

            if not produtos:
                print("Não há mais produtos cadastrados para serem deletados.")
                break
    else:
        print("Falha no login, não foi possível continuar.")

if __name__ == "__main__":
    main()
