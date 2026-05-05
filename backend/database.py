import sqlite3

def get_db_connection():
    conn = sqlite3.connect("safetrade.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        trust_score INTEGER DEFAULT 100
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        seller_email TEXT NOT NULL,
        FOREIGN KEY (seller_email) REFERENCES users(email)
    )
    """)

    conn.commit()
    conn.close()
