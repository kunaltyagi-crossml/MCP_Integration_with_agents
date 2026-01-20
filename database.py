import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trip_expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        amount INTEGER,
        description TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_expense(category, amount, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO trip_expenses
        (category, amount, description, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (category, amount, description, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()


def fetch_all_expenses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT category, amount, description FROM trip_expenses")
    rows = cursor.fetchall()

    conn.close()
    return rows
