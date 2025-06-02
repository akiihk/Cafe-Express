import os
from datetime import datetime
import random

produtos = []
numero_nota = random.randint(1, 9999)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_nome_do_programa():
    print('╔══════════════════════════╗')
    print('║  ☕  Café Express ☕     ║')  
    print('╚══════════════════════════╝\n')

def exibir_opcoes():
    print('1. Cadastrar produtos')
    print('2. Listar produtos')
    print('3. Ativar produtos')
    print('4. Desativar produtos')  
    print('5. Remover produtos')
    print('6. Emitir nota fiscal (teste)')
    print('7. Sair\n')

def finalizar_app():
    limpar_tela()
    resposta =input('Tem certeza que deseja finalizar o app? (S/N) ') 
    if resposta.lower() == 's':
        limpar_tela()
        print('Finalizando o app...')
    elif resposta.lower() == 'n':
        main()
    else:
        finalizar_app()

def voltar_ao_menu_principal():
    input('\nAperte enter para voltar ao menu principal')
    main()

def opcao_invalida():
    limpar_tela()
    print('Opção Inválida!\n')
    voltar_ao_menu_principal()

def cadastrar_novo_produto():
    limpar_tela()
    print('Cadastro de novos produtos\n')
    nome_do_produto = input('Digite o nome do produto que deseja cadastrar: ')
    if nome_do_produto in [p['nome'] for p in produtos]:
        limpar_tela()
        print(f"Produto '{nome_do_produto}' já está cadastrado, tente outro produto.")
        voltar_ao_menu_principal()

    elif nome_do_produto == '':
        opcao_invalida()
        
    else:
        produto = {'nome': nome_do_produto, 'ativo': False}
        produtos.append(produto)
        limpar_tela()
        print(f"O Produto '{nome_do_produto}' foi cadastrado com sucesso!")
        voltar_ao_menu_principal()

def listar_produtos():
    limpar_tela()
    if produtos:
        print("Produtos cadastrados:\n")
        for i, produto in enumerate(produtos, start = 1):
            status = '✅ Ativo' if produto['ativo'] else '❌ Inativo'
            print(f'{i}. {produto["nome"]} - {status}')
    else:
        print('Nenhum produto cadastrado.')
    voltar_ao_menu_principal()

def opcao_listagem():
    limpar_tela()
    print('1. Listar todos os produtos')
    print('2. Listar produtos ativos')
    print('3. Listar produtos desativados')
    print('4. Voltar ao menu principal')

def error_listagem():
    limpar_tela()
    input('Opção inválida, aperte enter para tentar novamente.')
    opcao_listagem()
    escolher_opcao_listagem()

def escolher_opcao_listagem():
    opcao = input('\nEscolha a forma de listagem: ')
    if opcao == '1':
        listar_produtos()
    elif opcao == '2':
        listar_produtos_ativos()
    elif opcao == '3':
        listar_produtos_desativados()
    elif opcao == '4':
        main()
    else:
        error_listagem()

def listar_produtos_ativos():
    limpar_tela()
    if produtos == True:
        print("Produtos ativos:\n")
        for i, produto in enumerate(produtos, start = 1):
            if produto['ativo']:
                print(f'{i}. {produto["nome"]}\n')
    else:
        print('Nehum produto ativado.')
    voltar_ao_menu_principal()

def listar_produtos_desativados():
    limpar_tela()
    if produtos == False:
        print("Produtos desativados:\n")
        for i, produto in enumerate(produtos, start = 1):
            if not produto['ativo']:
                print(f'{i}. {produto["nome"]}')
    else:
        print('Nenhum produto desativado.')
        voltar_ao_menu_principal()

def ativar_produtos():
    limpar_tela()
    if produtos:
        print("Produtos cadastrados:\n")
        for i, produto in enumerate(produtos, start = 1):
            print(f"{i}. {produto['nome']}")

        nome_do_produto = input("\nDigite o nome do produto que deseja ativar: ")

        for produto in produtos:
            if produto['nome'].lower() == nome_do_produto.lower():
                if produto['ativo']:
                    limpar_tela()
                    print(f"\nO produto '{produto['nome']}' já está ativado.")

                else:
                    limpar_tela()
                    produto['ativo'] = True
                    print(f"\nProduto '{produto['nome']}' ativado com sucesso!")
                voltar_ao_menu_principal()
            
        if nome_do_produto == '':
            opcao_invalida()
        
        limpar_tela()
        print(f"Produto '{nome_do_produto}' não encontrado na lista.")
    else:
        print('Nenhum produto cadastrado.')
    voltar_ao_menu_principal()

def desativar_produtos():
    limpar_tela()
    if produtos:
        print("Produtos cadastrados:\n")
        for i, produto in enumerate(produtos, start = 1):
            print(f"{i}. {produto['nome']}")

        nome_do_produto = input("\nDigite o nome do produto que deseja desativar: ")

        for produto in produtos:
            if produto['nome'].lower() == nome_do_produto.lower():
                if not produto['ativo']:
                    limpar_tela()
                    print(f"\nO produto '{produto['nome']}' já está desativado.")
                else:
                    limpar_tela()
                    produto['ativo'] = False
                    print(f"\nProduto '{produto['nome']}' desativado com sucesso!")
                voltar_ao_menu_principal()
            
        if nome_do_produto == '':
            opcao_invalida()

        limpar_tela()
        print(f"Produto '{nome_do_produto}' não encontrado na lista.")
    else:
        print('Nenhum produto cadastrado.')
    voltar_ao_menu_principal()

def remover_produto():
    limpar_tela()
    if produtos:
        print("Produtos cadastrados:\n")
        for i, produto in enumerate(produtos, start = 1):
            print(f"{i}. {produto['nome']}")

        nome_do_produto = input("\nDigite o nome do produto que deseja remover: ")

        for produto in produtos:
            if produto['nome'].lower() == nome_do_produto.lower():
                produtos.remove(produto)
                limpar_tela()
                print(f"Produto '{produto['nome']}' removido com sucesso!")
                voltar_ao_menu_principal()
                return

        limpar_tela()
        print(f"Produto {nome_do_produto} não encontrado na lista.")
    else:
        print('Nenhum produto cadastrado.')
    voltar_ao_menu_principal()

def emitir_nota_fiscal():
    global numero_nota
    limpar_tela()

    ativos = [p for p in produtos if isinstance(p, dict) and p.get('ativo')]

    if not produtos:
        print("Nenhum produto cadastrado.")
    elif not ativos:
        print("Nenhum produto ativado. Ative um produto antes de emitir uma nota.")
    else:
        print("Produtos ativos disponíveis para venda:\n")
        for i, p in enumerate(ativos, 1):
            print(f"{i}. {p['nome']}")
        
        nome = input("\nProduto vendido: ").strip().lower()
        if not any(p['nome'].lower() == nome for p in ativos):
            limpar_tela()
            print(f"Produto '{nome}' não encontrado na lista de produtos ativos.")
            voltar_ao_menu_principal()
            
        cliente = input("Cliente (opcional): ").strip()


        for p in ativos:
            if p['nome'].lower() == nome:
                valor = round(random.uniform(3.5, 20.0), 2)
                data = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                limpar_tela()
                print("🧾 Nota Fiscal (Teste)\n" + "═"*26)
                print(f"Nota nº: {numero_nota}")
                print(f"Data: {data}")
                print(f"Cliente: {cliente or 'Não informado'}")
                print(f"Produto: {p['nome']}")
                print(f"Valor: R$ {valor:.2f}")
                print("═"*26)
                numero_nota = random.randint(1, 9999)
                voltar_ao_menu_principal()

        print(f"\nProduto '{nome}' não está disponível ou não está ativo.")

    voltar_ao_menu_principal()

def escolher_opcao():
    try:
        opcao_escolhida = int(input('Escolha uma opção: '))
        if opcao_escolhida == 1:
            cadastrar_novo_produto()
        elif opcao_escolhida == 2:
            opcao_listagem()
            escolher_opcao_listagem()
        elif opcao_escolhida == 3:
            ativar_produtos()
        elif opcao_escolhida == 4:
            desativar_produtos()
        elif opcao_escolhida == 5:
            remover_produto()
        elif opcao_escolhida == 6:
            emitir_nota_fiscal()
        elif opcao_escolhida == 7:
            finalizar_app()
        else:
            opcao_invalida()
    except ValueError:
        opcao_invalida()

def main():
    limpar_tela()
    exibir_nome_do_programa()
    exibir_opcoes()
    escolher_opcao()

if __name__ == '__main__':
    main()
