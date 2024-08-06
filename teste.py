import sqlite3
from random import randint

def criar():
    conn = sqlite3.connect("databases/produtos.db")
    sql = """
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY, 
        nome TEXT, 
        descricao TEXT, 
        preco TEXT, 
        link TEXT, 
        imagem TEXT
    )
    """
    conn.execute(sql)
    print("\nTabela criada com sucesso\n")
    conn.close()

def tudo():
    conn = sqlite3.connect("databases/produtos.db")
    sql = "SELECT * FROM produtos"
    cursor = conn.execute(sql)
    for row in cursor:
        print(row)
    conn.close()
    print('\n---------------------\n')

def inserir(id, nome, descricao, preco, link, imagem):
    conn = None
    try:
        conn = sqlite3.connect("databases/produtos.db")
        sql = "INSERT INTO produtos (id, nome, descricao, preco, link, imagem) VALUES (?, ?, ?, ?, ?, ?)"
        conn.execute(sql, (id, nome, descricao, preco, link, imagem))
        conn.commit()
        print("\nRegistro inserido com sucesso\n")
    except sqlite3.IntegrityError as e:
        print(f"Erro de integridade: {e}")
    except sqlite3.OperationalError as e:
        print(f"Erro operacional: {e}")
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        if conn:
            conn.close()
            print("\nConexão fechada\n")

def atualizar(id, nome, descricao, preco, link, imagem):
    conn = None
    try:
        conn = sqlite3.connect("databases/produtos.db")
        sql = "UPDATE produtos SET nome = ?, descricao = ?, preco = ?, link = ?, imagem = ? WHERE id = ?"
        conn.execute(sql, (nome, descricao, preco, link, imagem, id))
        conn.commit()
        print("\nRegistro atualizado com sucesso\n")
    except sqlite3.IntegrityError as e:
        print(f"Erro de integridade: {e}")
    except sqlite3.OperationalError as e:
        print(f"Erro operacional: {e}")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar dados: {e}")
    finally:
        if conn:
            conn.close()
            print("\nConexão fechada\n")

def deletar(id):
    conn = None
    try:
        conn = sqlite3.connect("databases/produtos.db")
        sql = "DELETE FROM produtos WHERE id = ?"
        conn.execute(sql, (id,))
        conn.commit()
        print("Registro deletado com sucesso")
    except sqlite3.Error as e:
        print(f"Erro ao deletar dados: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexão fechada")

def sair():
    print("\nSaindo do programa...\n")

# Opções do menu
print("Digite o que deseja fazer\n1 - Selecionar tudo\n2 - Criar tabela\n3 - Inserir dados\n4 - Atualizar dados\n5 - Deletar dados\n6 - Sair")
entrada = input(': ')

if entrada == "1" or entrada.lower() == "tudo":
    tudo()

elif entrada == "2" or entrada.lower() == "criar":
    criar()

elif entrada == "3" or entrada.lower() == "inserir":
    id = randint(1, 10000)
    nome = input("Digite o nome: ")
    descricao = input("Digite a descrição: ")
    preco = input("Digite o preço: ")
    link = input("Digite o link: ")
    imagem = input("Digite a imagem: ")
    inserir(id, nome, descricao, preco, link, imagem)

elif entrada == "4" or entrada.lower() == "atualizar":
    id = int(input("Digite o id: "))
    nome = input("Digite o nome: ")
    descricao = input("Digite a descrição: ")
    preco = input("Digite o preço: ")
    link = input("Digite o link: ")
    imagem = input("Digite a imagem: ")
    atualizar(id, nome, descricao, preco, link, imagem)

elif entrada == "5" or entrada.lower() == "deletar":
    id = int(input("Digite o id: "))
    deletar(id)

elif entrada == "6" or entrada.lower() == "sair":
    sair()

else:
    print("Opção inválida. Tente novamente.")
