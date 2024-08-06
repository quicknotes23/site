import sqlite3
import json
from flask import jsonify

def get_db_connection():
    conn = sqlite3.connect("databases/produtos.db")
    conn.row_factory = sqlite3.Row
    return conn

def select():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    rows = cursor.fetchall()
    conn.close()
    return rows

def info():
    resposta = select()
    dados = [dict(row) for row in resposta]  # Convertendo para dicionário
    return jsonify(dados)  # Retorna uma resposta JSON
