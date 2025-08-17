# database.py
import sqlite3
from datetime import datetime

DB = 'Database/Expense_Planner.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL
        )''')

def email_exists(email):
    with sqlite3.connect(DB) as conn:
        result = conn.execute('SELECT 1 FROM users WHERE email=?', (email,)).fetchone()
        return bool(result)

def add_user(name, email, password):
    if email_exists(email):
        return False
    try:
        with sqlite3.connect(DB) as conn:
            conn.execute(
                'INSERT INTO users (name, email, password, created_at) VALUES (?,?,?,?)',
                (name, email, password, datetime.now())
            )
            return True
    except:
        return False

def validate_login(email, password):
    with sqlite3.connect(DB) as conn:
        user = conn.execute(
            'SELECT id, name, password FROM users WHERE email=?', 
            (email,)
        ).fetchone()
        if user and user[2] == password:  # In production, use proper password hashing
            return {'id': user[0], 'name': user[1]}
        return None