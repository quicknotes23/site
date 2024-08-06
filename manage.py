import sqlite3
from random import randint

DATABASE = "databases/produtos.db"

def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def criar():
    conn = connect_db()
    sql = """
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        preco TEXT,
        link TEXT,
        imagem TEXT
    )
    """
    try:
        conn.execute(sql)
        conn.commit()
        print("\nTabela criada com sucesso\n")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        conn.close()

def tudo():
    conn = connect_db()
    sql = "SELECT * FROM produtos"
    try:
        cursor = conn.execute(sql)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar dados: {e}")
        return []
    finally:
        conn.close()

def inserir(nome, descricao, preco, link, imagem):
    conn = connect_db()
    sql = "INSERT INTO produtos (nome, descricao, preco, link, imagem) VALUES (?, ?, ?, ?, ?)"
    try:
        conn.execute(sql, (nome, descricao, preco, link, imagem))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        conn.close()

def atualizar(id, nome, descricao, preco, link, imagem):
    conn = connect_db()
    sql = "UPDATE produtos SET nome = ?, descricao = ?, preco = ?, link = ?, imagem = ? WHERE id = ?"
    try:
        conn.execute(sql, (nome, descricao, preco, link, imagem, id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao atualizar dados: {e}")
    finally:
        conn.close()

def deletar(id):
    conn = connect_db()
    sql = "DELETE FROM produtos WHERE id = ?"
    try:
        conn.execute(sql, (id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao deletar dados: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: manage.py [comando] [argumentos]")
        sys.exit(1)

    comando = sys.argv[1]

    if comando == "criar":
        criar()
    elif comando == "tudo":
        for row in tudo():
            print(row)
    elif comando == "inserir":
        if len(sys.argv) != 7:
            print("Uso: manage.py inserir [nome] [descricao] [preco] [link] [imagem]")
            sys.exit(1)
        inserir(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    elif comando == "atualizar":
        if len(sys.argv) != 8:
            print("Uso: manage.py atualizar [id] [nome] [descricao] [preco] [link] [imagem]")
            sys.exit(1)
        atualizar(int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
    elif comando == "deletar":
        if len(sys.argv) != 3:
            print("Uso: manage.py deletar [id]")
            sys.exit(1)
        deletar(int(sys.argv[2]))
    else:
        print("Comando inválido.")
