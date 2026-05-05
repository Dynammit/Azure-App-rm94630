from flask import Flask, render_template, request, redirect
import pyodbc
import os

app = Flask(__name__)

# CONFIGURAÇÃO DO BANCO (ajuste com seus dados da Azure)
server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
# NÃO UTILIZE OS CARACTERES: "@", "!", "&" NA SENHA -> Gera problemas na conexão
password = os.getenv("DB_PASSWORD")

conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
)

def get_connection():
    return pyodbc.connect(conn_str)

@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contatos")
    dados = cursor.fetchall()
    conn.close()
    return render_template('index.html', dados=dados)

@app.route('/add', methods=['POST'])
def add():
    nome = request.form['nome']
    email = request.form['email']
    celular = request.form['celular']

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contatos (nome, email, celular) VALUES (?, ?, ?)",
                   (nome, email, celular))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contatos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contatos WHERE id = ?", (id,))
    dado = cursor.fetchone()
    conn.close()

    return render_template('edit.html', dado=dado)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    nome = request.form['nome']
    email = request.form['email']
    celular = request.form['celular']

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE contatos
        SET nome=?, email=?, celular=?
        WHERE id=?
    """, (nome, email, celular, id))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
