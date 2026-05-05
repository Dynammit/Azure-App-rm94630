from flask import Flask, render_template, request, redirect
import pyodbc
import os

app = Flask(__name__)


server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")

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
    
    cursor.execute("SELECT * FROM estoque_inova")
    dados = cursor.fetchall()
    conn.close()
    return render_template('index.html', dados=dados)

@app.route('/add', methods=['POST'])
def add():
  
    id_peca = request.form['id']
    sku = request.form['sku']
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    preco = request.form['preco']

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO estoque_inova (Id, SKU, Nome, Quantidade, Preco) 
        VALUES (?, ?, ?, ?, ?)
    """, (id_peca, sku, nome, quantidade, preco))
    
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_connection()
    cursor = conn.cursor()
   
    cursor.execute("DELETE FROM estoque_inova WHERE Id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn = get_connection()
    cursor = conn.cursor()
  
    cursor.execute("SELECT * FROM estoque_inova WHERE Id = ?", (id,))
    dado = cursor.fetchone()
    conn.close()

    return render_template('edit.html', dado=dado)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
   
    sku = request.form['sku']
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    preco = request.form['preco']

    conn = get_connection()
    cursor = conn.cursor()
   
    cursor.execute("""
        UPDATE estoque_inova
        SET SKU=?, Nome=?, Quantidade=?, Preco=?
        WHERE Id=?
    """, (sku, nome, quantidade, preco, id))
    
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
