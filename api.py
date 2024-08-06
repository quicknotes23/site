import sqlite3
import json
from flask import jsonify


conn = sqlite3.connect("databases/produtos.db")
cursor = conn.cursor()

def select(id):
    cursor.execute("SELECT id FROM produtos")
    rows = cursor.fetchone()
    return rows

def info():
  resposta = select(id)
  dados = resposta.json()