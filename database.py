import sqlite3
from datetime import date

DB_FILE = "meusaldo.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spendings (
        spending_id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        value TEXT NOT NULL,
        date TEXT NOT NULL
        )
    """)

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


def get_spendings(
        start_date: date | None = None,
        end_date: date | None = None,
        category: str | None = None,
    ):

    conn = get_connection()
    cursor = conn.cursor()

    conditions = []
    values = []

    if category is not None:
        conditions.append("category = ?")
        values.append(category)

    if start_date is not None:
        conditions.append("date(date) >= ?")
        values.append(start_date.isoformat())

    if end_date is not None:
        conditions.append("date(date) <= ?")
        values.append(end_date.isoformat())

    query = "SELECT * FROM spendings"

    if conditions:    
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, values)
    
    spendings = cursor.fetchall()
    conn.close()
    return spendings


def get_spending_by_id(spending_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spendings WHERE spending_id = ?", (spending_id,))
    spending = cursor.fetchone()
    conn.close()
    return spending


def update_spending(
    spending_id: int, description: str, category: str, value: str, date: str
):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE spendings SET description = ?, category = ?, value = ?, date = ? WHERE spending_id = ?",
        (description, category, value, date, spending_id),
    )

    rows_affected = cursor.rowcount

    conn.commit()
    conn.close()
    return rows_affected


def delete_spending(spending_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM spendings WHERE spending_id = ?", (spending_id,))

    rows_affected = cursor.rowcount

    conn.commit()
    conn.close()

    return rows_affected


def get_month_spendings(year: int, month: int):
    conn = get_connection()
    cursor = conn.cursor()

    mes = f"{year:04d}-{month:02d}"

    cursor.execute("SELECT value FROM spendings WHERE strftime('%Y-%m', date) = ?", (mes,))

    spendings = cursor.fetchall()

    conn.close()

    return spendings
