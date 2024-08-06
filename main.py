from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import logging
import spacy
from api import info  # Importa a função info do api.py
from typing import List
from manage import inserir, atualizar, deletar, tudo

app = Flask(__name__)
app.secret_key = 'e5y53heamyusdfh'  # Chave secreta para a sessão

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dados de autenticação simples
USERNAME = 'quicknotes527@gmail.com'
PASSWORD = 'danilo123'

# Carregar o modelo de língua do spaCy
nlp = spacy.load('pt_core_news_sm')

def get_db_connection() -> List[dict]:
    """Retorna todos os produtos do banco de dados."""
    return tudo()

def lemmatize_query(query: str) -> str:
    """Retorna a consulta lematizada para busca eficiente."""
    doc = nlp(query)
    return ' '.join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sobre')
def about():
    return render_template("sobre.html")

@app.route('/api')
def api():
    return info()  # Chama a função info que retorna JSON

@app.route('/produtos')
def produtos():
    query = request.args.get('query', '').strip().lower()
    lemmatized_query = lemmatize_query(query)
    words = lemmatized_query.split()

    produtos = get_db_connection()

    try:
        if words:
            conditions = ' OR '.join(['LOWER(nome) LIKE ? OR LOWER(descricao) LIKE ?' for _ in words])
            parameters = ['%' + word + '%' for word in words for _ in (0, 1)]
            produtos = [p for p in produtos if any(word in p['nome'].lower() or word in p['descricao'].lower() for word in words)]
        else:
            produtos = produtos
    except Exception as e:
        logger.error(f"Erro ao consultar dados: {e}")
        produtos = []

    return render_template("produtos.html", produtos=produtos, query=query)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            if username == USERNAME and password == PASSWORD:
                session['logged_in'] = True
                return redirect(url_for('admin'))
            else:
                return render_template('login.html', error='Usuário ou senha inválidos')
        except Exception as e:
            logger.error(f"Erro ao processar login: {e}")
            return render_template('login.html', error='Erro ao processar o login')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            if 'add' in request.form:
                nome = request.form['nome']
                descricao = request.form['descricao']
                preco = request.form['preco']
                link = request.form['link']
                imagem = request.form['imagem']

                inserir(nome=nome, descricao=descricao, preco=preco, link=link, imagem=imagem)

            elif 'update' in request.form:
                product_id = request.form['id']
                nome = request.form['nome']
                descricao = request.form['descricao']
                preco = request.form['preco']
                link = request.form['link']
                imagem = request.form['imagem']

                current_image = request.form.get('current_image', '')
                imagem_path = imagem if imagem else current_image

                atualizar(id=product_id, nome=nome, descricao=descricao, preco=preco, link=link, imagem=imagem_path)

            elif 'delete' in request.form:
                product_id = request.form['id']
                deletar(id=product_id)

        except Exception as e:
            logger.error(f"Erro ao processar dados: {e}")

        return redirect(url_for('admin'))

    produtos = get_db_connection()

    return render_template("admin.html", produtos=produtos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
