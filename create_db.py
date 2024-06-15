import sqlite3
import os

def connect_db():
    # Obter o diretório atual do script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(current_dir, 'database', 'bank.db')

    conn = sqlite3.connect(database_path)
    return conn

def create_database_if_not_exists():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    database_dir = os.path.join(current_dir, 'database')
    database_path = os.path.join(database_dir, 'bank.db')

    if not os.path.exists(database_dir):
        os.makedirs(database_dir)

    with sqlite3.connect(database_path) as conn:
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

    print("Banco de dados e tabela criados com sucesso.")

if __name__ == '__main__':
    create_database_if_not_exists()
