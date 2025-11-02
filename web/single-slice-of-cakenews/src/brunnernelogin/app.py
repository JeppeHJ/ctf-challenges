from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import jwt
import os
import re
from database_bl import init_db, get_user_by_credentials, create_user, get_db_connection

app = Flask(__name__)
CORS(app)

PORT = os.environ.get('BRUNNERNELOGIN_PORT', 5000)
SECRET_KEY = os.environ.get('BRUNNERNELOGIN_SECRET')
EMAIL_REGEX = re.compile(r'^[\w\.+-]+@[\w.-]+\.[a-zA-Z]{2,}$')

def current_user_from_request():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    token = auth_header[7:]
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/profile')
def sso_profile():
    return render_template('profile.html')

@app.route('/api/profile', methods=['GET'])
def api_profile():
    user = current_user_from_request()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    user_id = user.get('user_id')
    conn = get_db_connection()
    c = conn.cursor()
    row = c.execute('SELECT email, flag FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'not_found'}), 404
    email, flag = row
    return jsonify({'email': email, 'flag': flag})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password', '')
    if not EMAIL_REGEX.match(email):
        return jsonify({'error': 'invalid_email'}), 400

    user = get_user_by_credentials(email, password)

    if user:
        token = jwt.encode({
            'user_id': user[0],
            'email': user[1]
        }, SECRET_KEY, algorithm='HS256')

        return jsonify({'token': token})

    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not EMAIL_REGEX.match(email):
        return jsonify({'error': 'invalid_email'}), 400

    if not email or not password:
        return jsonify({'error': 'email and password required'}), 400

    if create_user(email, password):
        return jsonify({'success': True}), 201
    else:
        return jsonify({'error': 'email_taken'}), 409

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=PORT)
