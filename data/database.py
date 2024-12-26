import sqlite3
from datetime import datetime

DB_NAME = "data/userdata.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS log_book (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            activity TEXT,
            metamask_account TEXT UNIQUE,
            name TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(metamask_account, password, activity, name=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO log_book (datetime, activity, metamask_account, name, password) 
        VALUES (?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), activity, metamask_account, name, password))
    conn.commit()
    conn.close()

def check_user_exists(metamask_account):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM log_book WHERE metamask_account = ?", (metamask_account,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def validate_user(metamask_account, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM log_book WHERE metamask_account = ? AND password = ?", (metamask_account, password))
    valid = cursor.fetchone() is not None
    conn.close()
    return valid
