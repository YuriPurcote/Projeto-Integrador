import sys
import webbrowser
import sqlite3
import os
import logging
from flask import Flask, render_template, request, redirect, url_for


# Obtém o caminho absoluto do diretório onde o script está sendo executado
current_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Define o caminho absoluto para o diretório de templates
template_dir = os.path.join(current_dir, 'templates')

# Configura o Flask com o caminho absoluto para o diretório de templates
app = Flask(__name__, template_folder=template_dir)
# Configuração básica de logging
logging.basicConfig(level=logging.DEBUG)
def connect_db():
    # Obter o caminho absoluto para o banco de dados
    database_path = os.path.join(current_dir, 'bank.db')

    # Verificar se o diretório do banco de dados existe; se não, criar
    if not os.path.exists(os.path.dirname(database_path)):
        os.makedirs(os.path.dirname(database_path))

    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    # Criar a tabela 'transactions' se ela não existir
    cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

    return sqlite3.connect(database_path)

def format_currency(value):
    return '{:,.2f}'.format(value).replace(',', 'v').replace('.', ',').replace('v', '.')

@app.template_filter('format_currency')
def format_currency_filter(value):
    return format_currency(value)

@app.route('/')
def index():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute('SELECT * FROM transactions ORDER BY timestamp DESC')
    transactions = cur.fetchall()

    cur.execute('SELECT SUM(amount) FROM transactions')
    balance = cur.fetchone()[0] or 0.0

    conn.close()
    return render_template('index.html', transactions=transactions, balance=balance)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    amount = float(request.form['amount'])
    transaction_type = request.form['transaction_type']

    if transaction_type == 'withdraw':
        amount = -amount

    conn = connect_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO transactions (amount, type) VALUES (?, ?)', (amount, transaction_type))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/edit_transaction/<int:id>', methods=['GET'])
def edit_transaction(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM transactions WHERE id = ?', (id,))
    transaction = cur.fetchone()
    conn.close()

    return render_template('edit_transaction.html', transaction=transaction)

@app.route('/update_transaction/<int:id>', methods=['POST'])
def update_transaction(id):
    amount = float(request.form['amount'])
    transaction_type = request.form['transaction_type']

    if transaction_type == 'withdraw':
        amount = -amount

    conn = connect_db()
    cur = conn.cursor()
    cur.execute('UPDATE transactions SET amount = ?, type = ? WHERE id = ?', (amount, transaction_type, id))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/delete_transaction/<int:id>', methods=['POST'])
def delete_transaction(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM transactions WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    # Iniciar o servidor Flask
    app.run(debug=True)
