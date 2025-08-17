# app.py
from flask import Flask, request, jsonify, send_from_directory, session, render_template, redirect
from database.database import init_db, add_user, email_exists, validate_login
import os

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = os.urandom(24)

# Initialize DB
init_db()

# -----------------------------
# Serve Static Files
# -----------------------------
@app.route('/')
def home():
    return send_from_directory('templates', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# -----------------------------
# Signup Route
# -----------------------------
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    if not all([name, email, password]):
        return jsonify(error='All fields (name, email, password) are required.'), 400

    if email_exists(email):
        return jsonify(error='Email is already registered.'), 409

    if add_user(name, email, password):
        return jsonify(message='Signup successful.'), 201
    else:
        return jsonify(error='Signup failed.'), 500

# -----------------------------
# Login Route
# -----------------------------
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    if not all([email, password]):
        return jsonify(error='Email and password are required.'), 400

    user = validate_login(email, password)
    if not user:
        return jsonify(error='Invalid email or password.'), 401

    session['user_id'] = user['id'] if isinstance(user, dict) and 'id' in user else user[0]
    session['user_name'] = user['name'] if isinstance(user, dict) and 'name' in user else user[1]

    return jsonify(redirect='/First_Page.html', name=session['user_name']), 200

@app.route('/api/auth/logout')
def logout():
    session.clear()
    return jsonify(message='Logged out successfully'), 200

# -----------------------------
# Run Flask Server
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5050)