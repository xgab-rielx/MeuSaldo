from datetime import date

import os
import psycopg
from psycopg.rows import dict_row


def get_connection():
    return psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row, prepare_threshold=None)


def create_spending(user_id: int, description: str, category: str, value: str, date: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO spendings (user_id, description, category, value, date) VALUES (%s, %s, %s, %s, %s) RETURNING spending_id",
        (user_id, description, category, value, date),
    )
    spending_id = cursor.fetchone()["spending_id"]
    conn.commit()
    conn.close()
    return spending_id


def get_spendings(
        user_id: int,
        start_date: date | None = None,
        end_date: date | None = None,
        category: str | None = None,
    ):

    conn = get_connection()
    cursor = conn.cursor()

    conditions = ["user_id = %s"]
    values = [user_id]

    if category is not None:
        conditions.append("category = %s")
        values.append(category)

    if start_date is not None:
        conditions.append("SUBSTRING(date FROM 1 FOR 10) >= %s")
        values.append(start_date.isoformat())

    if end_date is not None:
        conditions.append("SUBSTRING(date FROM 1 FOR 10) <= %s")
        values.append(end_date.isoformat())

    query = "SELECT * FROM spendings"

    if conditions:    
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, values)
    
    spendings = cursor.fetchall()
    conn.close()
    return spendings


def get_spending_by_id(spending_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spendings WHERE spending_id = %s AND user_id = %s" , (spending_id, user_id),)
    spending = cursor.fetchone()
    conn.close()
    return spending


def update_spending(
    spending_id: int, user_id: int, description: str, category: str, value: str, date: str
):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE spendings SET description = %s, category = %s, value = %s, date = %s WHERE spending_id = %s AND user_id = %s",
        (description, category, value, date, spending_id, user_id),
    )

    rows_affected = cursor.rowcount

    conn.commit()
    conn.close()
    return rows_affected


def delete_spending(spending_id: int, user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM spendings WHERE spending_id = %s AND user_id = %s", (spending_id, user_id))

    rows_affected = cursor.rowcount

    conn.commit()
    conn.close()

    return rows_affected


def get_month_spendings(year: int, month: int, user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    mes = f"{year:04d}-{month:02d}"

    cursor.execute("SELECT value FROM spendings WHERE SUBSTRING(date FROM 1 FOR 7) = %s AND user_id = %s", (mes, user_id))

    spendings = cursor.fetchall()

    conn.close()

    return spendings


def create_user(username, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING user_id",
        (username, password_hash,),
    )
    user_id = cursor.fetchone()["user_id"]
    conn.commit()
    conn.close()
    return user_id

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()
    return user
