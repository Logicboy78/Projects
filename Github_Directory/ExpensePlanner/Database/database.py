# database.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'Expense_Planner.db')

# -----------------------------
# Initialize Database
# -----------------------------
def init_db():
    """Ensure the SQLite database and users table exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

# -----------------------------
# Add user
# -----------------------------
def add_user(name, email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?);",
        (name, email, password)
    )
    conn.commit()
    conn.close()

# -----------------------------
# Get user by email
# -----------------------------
def get_user_by_email(email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT password, name FROM users WHERE email = ?;", (email,)
    )
    row = c.fetchone()
    conn.close()
    return row