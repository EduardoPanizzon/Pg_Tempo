import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "app.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    with open(os.path.join(os.path.dirname(__file__), "schema.sql"), "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_PATH)
