import sqlite3

DB_FILE = "meusaldo.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS spendings (
        spending_id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        value TEXT NOT NULL,
        date TEXT NOT NULL
        )
    """
    )

    conn.commit()
    conn.close()


def create_spending(description: str, category: str, value: str, date: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO spendings (description, category, value, date) VALUES (?, ?, ?, ?)",
        (description, category, value, date),
    )
    conn.commit()
    spending_id = cursor.lastrowid
    conn.close()
    return spending_id

def get_spendings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spendings")
    spendings = cursor.fetchall()
    conn.close()
    return spendings

def get_spending_by_id(spending_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM spendings WHERE spending_id = ?",
        (spending_id,)    
    )
    spending = cursor.fetchone()
    conn.close()
    return spending