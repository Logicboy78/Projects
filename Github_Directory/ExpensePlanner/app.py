import os
import sqlite3
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')

DB_PATH = 'Expense_Planner.db'

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

init_db()

# -----------------------------
# Signup Route
# -----------------------------
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    name     = data.get('name', '').strip()
    email    = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    # Validate input
    if not name or not email or not password:
        return jsonify(error='All fields (name, email, password) are required.'), 400

    # DEV ONLY: store plaintext passwords for easy DB view
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?);",
            (name, email, password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify(error='Email is already registered.'), 409
    finally:
        conn.close()

    return jsonify(message='Signup successful.'), 201

# -----------------------------
# Login Route
# -----------------------------
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email    = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify(error='Email and password are required.'), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT password, name FROM users WHERE email = ?;",
        (email,)
    )
    row = c.fetchone()
    conn.close()

    # Compare plaintext passwords (dev mode)
    if not row or row[0] != password:
        return jsonify(error='Invalid email or password.'), 401

    # On success, send redirect instruction
    return jsonify(redirect='/First_Page.html', name=row[1]), 200

# -----------------------------
# Serve Static Files
# -----------------------------
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# -----------------------------
# Run Flask Server
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)