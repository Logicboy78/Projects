# app.py
from flask import Flask, request, jsonify, send_from_directory
from Database.database import init_db, add_user, get_user_by_email, verify_password

app = Flask(__name__, static_folder='.', static_url_path='')

# Initialize DB
init_db()

# -----------------------------
# Serve Static Files
# -----------------------------
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

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

    if add_user(name, email, password):
        return jsonify(message='Signup successful.'), 201
    else:
        return jsonify(error='Email is already registered.'), 409

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

    user = get_user_by_email(email)
    if not user or not verify_password(user['password'], password):
        return jsonify(error='Invalid email or password.'), 401

    return jsonify(redirect='/First_Page.html', name=user['name']), 200

# -----------------------------
# Run Flask Server
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    app.run(host='0.0.0.0', port=3000, debug=True)