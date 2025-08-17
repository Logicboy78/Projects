# database.py
import sqlite3
import os
import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'Expense_Planner.db')

def get_db():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# Initialize Database
# -----------------------------
def init_db():
    """Ensure all required tables exist."""
    with get_db() as conn:
        c = conn.cursor()
        # Users table
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # Categories table
        c.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """)
        
        # Expenses table
        c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (category_id) REFERENCES categories (id)
        );
        """)
        
        conn.commit()

# -----------------------------
# User Management
# -----------------------------
def add_user(name, email, password):
    """Add a new user"""
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?);",
                (name, email, password)  # Store password as plain text for testing
            )
            return True
    except sqlite3.IntegrityError:
        return False

def get_user_by_email(email):
    """Get user by email"""
    with get_db() as conn:
        c = conn.cursor()
        c.execute(
            "SELECT id, password, name FROM users WHERE email = ?;", 
            (email,)
        )
        user = c.fetchone()
        if user:
            return dict(user)
        return None

def verify_password(stored_password, provided_password):
    """Verify password (plain text comparison for testing)"""
    return stored_password == provided_password

# -----------------------------
# Category Management
# -----------------------------
def add_category(user_id, name):
    """Add a new expense category"""
    with get_db() as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO categories (user_id, name) VALUES (?, ?);",
            (user_id, name)
        )
        return c.lastrowid

def get_categories(user_id):
    """Get all categories for a user"""
    with get_db() as conn:
        c = conn.cursor()
        c.execute(
            "SELECT id, name FROM categories WHERE user_id = ? ORDER BY name;",
            (user_id,)
        )
        return [dict(row) for row in c.fetchall()]

# -----------------------------
# Expense Management
# -----------------------------
def add_expense(user_id, category_id, amount, description, date=None):
    """Add a new expense"""
    if date is None:
        date = datetime.datetime.now().date()
    
    with get_db() as conn:
        c = conn.cursor()
        c.execute(
            """INSERT INTO expenses 
            (user_id, category_id, amount, description, date) 
            VALUES (?, ?, ?, ?, ?);""",
            (user_id, category_id, amount, description, date)
        )
        return c.lastrowid

def get_expenses(user_id, start_date=None, end_date=None, category_id=None):
    """Get expenses with optional filters"""
    query = """
    SELECT e.*, c.name as category_name 
    FROM expenses e 
    JOIN categories c ON e.category_id = c.id 
    WHERE e.user_id = ?
    """
    params = [user_id]
    
    if start_date:
        query += " AND e.date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND e.date <= ?"
        params.append(end_date)
    if category_id:
        query += " AND e.category_id = ?"
        params.append(category_id)
    
    query += " ORDER BY e.date DESC"
    
    with get_db() as conn:
        c = conn.cursor()
        c.execute(query, params)
        return [dict(row) for row in c.fetchall()]