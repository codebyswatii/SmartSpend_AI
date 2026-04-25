import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "expenses.db")

def init_db():
    conn = sqlite3.connect("DB_PATH")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        amount INTEGER,
        category TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_expense(text, amount, category):
    init_db()  # 🔥 ensures table exists
    conn = sqlite3.connect("DB_PATH")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (text, amount, category) VALUES (?, ?, ?)",
        (text, amount, category)
    )

    conn.commit()
    conn.close()

#########################################
def delete_last_expense():
    conn = sqlite3.connect("DB_PATH")
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM expenses
        WHERE id = (SELECT MAX(id) FROM expenses)
    """)
    
    conn.commit()
    conn.close()

#########################################

def get_all_expenses():
    conn = sqlite3.connect("DB_PATH")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    data = cursor.fetchall()

    conn.close()
    return data