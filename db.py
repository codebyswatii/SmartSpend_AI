import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "expenses.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        text TEXT,
        amount INTEGER,
        category TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_expense(user_id, text, amount, category):
    init_db()  # 🔥 ensures table exists
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 🔥 FORCE TABLE CREATION HERE (same connection)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        text TEXT,
        amount INTEGER,
        category TEXT
    )
    """)

    cursor.execute(
        "INSERT INTO expenses (user_id, text, amount, category) VALUES (?, ?, ?, ?)",
        (user_id, text, amount, category)
    )

    conn.commit()
    conn.close()

#########################################
def delete_last_expense(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM expenses
        WHERE id = (
            SELECT MAX(id) FROM expenses WHERE user_id = ?
        )
    """, (user_id,))
    
    conn.commit()
    conn.close()

#########################################

def get_all_expenses(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE user_id = ?", (user_id,))
    data = cursor.fetchall()

    conn.close()
    return data