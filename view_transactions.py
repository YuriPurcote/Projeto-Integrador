import sqlite3

def view_transactions():
    conn = sqlite3.connect('./bank.db')
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM transactions')
    rows = cur.fetchall()
    
    conn.close()
    
    return rows

if __name__ == "__main__":
    transactions = view_transactions()
    for transaction in transactions:
        print(transaction)
