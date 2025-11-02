from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from database import init_db, get_db_connection
import os
import requests
import jwt, datetime
import re
import bleach

PORT = os.environ.get('CAKENEWS_PORT', 5000)
BRUNNERNELOGIN_BASE_URL = os.environ.get('BRUNNERNELOGIN_BASE_URL', 'http://brunnernelogin:5000')
SECRET_KEY = os.environ.get('CAKENEWS_SECRET')
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

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/article/<int:article_id>')
def article_detail(article_id):
    return render_template('article.html', article_id=article_id)

@app.route('/static/images/<filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/api/articles', methods=['GET'])
def get_articles():
    conn = get_db_connection()
    c = conn.cursor()
    articles = c.execute('SELECT * FROM articles ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([{
        'id': a[0],
        'title': a[1],
        'content': a[2],
        'author': a[3],
        'category': a[4],
        'image_url': a[5],
        'created_at': a[6]
    } for a in articles])

@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    conn = get_db_connection()
    c = conn.cursor()
    article = c.execute('SELECT * FROM articles WHERE id = ?', (article_id,)).fetchone()
    conn.close()

    if article:
        return jsonify({
            'id': article[0],
            'title': article[1],
            'content': article[2],
            'author': article[3],
            'category': article[4],
            'image_url': article[5],
            'created_at': article[6]
        })
    return jsonify({'error': 'Article not found'}), 404

@app.route('/api/articles/<int:article_id>/comments', methods=['GET'])
def get_article_comments(article_id):
    conn = get_db_connection()
    c = conn.cursor()
    comments = c.execute(
        'SELECT * FROM comments WHERE article_id = ? ORDER BY created_at DESC',
        (article_id,)
    ).fetchall()
    conn.close()
    return jsonify([{
        'id': c[0],
        'article_id': c[1],
        'username': c[2],
        'content': c[3],
        'created_at': c[4]
    } for c in comments])

@app.route('/api/register', methods=['POST'])
def api_register():

    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    conf = data.get('password_confirmation', '')

    if not EMAIL_REGEX.match(email):
        return jsonify({'error': 'invalid_email'}), 400

    if not all([email, username, password, conf]):
        return jsonify({'error': 'missing_fields'}), 400
    if password != conf:
        return jsonify({'error': 'password_mismatch'}), 400

    try:
        sso_resp = requests.post(
            f"{BRUNNERNELOGIN_BASE_URL}/api/register",
            json={'email': email, 'password': password}, timeout=5
        )
    except requests.exceptions.RequestException:
        return jsonify({'error': 'sso_unreachable'}), 502

    if sso_resp.status_code == 409:
        return jsonify({'error': 'email_taken'}), 409
    if sso_resp.status_code != 201:
        return jsonify({'error': 'sso_error', 'details': sso_resp.text}), 500

    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (email, username, role) VALUES (?, ?, ?)', (email, username, 'user'))
        conn.commit()
    except Exception as exc:
        conn.rollback()
        return jsonify({'error': 'username_taken_or_db_error', 'details': str(exc)}), 409
    finally:
        conn.close()

    return jsonify({'success': True}), 201

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    if not EMAIL_REGEX.match(email):
        return jsonify({'error': 'invalid_email'}), 400
    if not email or not password:
        return jsonify({'error': 'missing_fields'}), 400

    try:
        sso_resp = requests.post(f"{BRUNNERNELOGIN_BASE_URL}/api/login", json={'email': email, 'password': password, 'redirect': ''}, timeout=5)
    except requests.exceptions.RequestException:
        return jsonify({'error': 'sso_unreachable'}), 502
    if sso_resp.status_code != 200:
        return jsonify({'error': 'invalid_credentials'}), 401

    conn = get_db_connection()
    c = conn.cursor()
    user = c.execute('SELECT username, role FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    if not user:
        return jsonify({'error': 'no_local_profile'}), 404
    username, role = user

    token = jwt.encode({
        'email': email,
        'username': username,
        'role': role,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({'token': token, 'username': username, 'role': role})

@app.route('/api/profile', methods=['GET'])
def api_profile():
    user = current_user_from_request()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    return jsonify({
        'email': user.get('email'),
        'username': user.get('username'),
        'role': user.get('role')
    })

@app.route('/api/articles/<int:article_id>/report-journalist', methods=['POST'])
def report_to_journalist(article_id):
    user = current_user_from_request()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    if user.get('role') != 'user':
        return jsonify({'error': 'forbidden'}), 403

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO reports (article_id, level) VALUES (?, ?)', (article_id, 'journalist'))
    conn.commit()
    conn.close()

    print(f"[REPORT] Article {article_id} reported to journalist by {user['username']}")
    return jsonify({'success': True})

@app.route('/api/articles/<int:article_id>/report-admin', methods=['POST'])
def report_to_admin(article_id):
    user = current_user_from_request()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401
    if user.get('role') != 'journalist':
        return jsonify({'error': 'forbidden'}), 403

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO reports (article_id, level) VALUES (?, ?)', (article_id, 'admin'))
    conn.commit()
    conn.close()

    print(f"[REPORT] Article {article_id} escalated to admin by journalist {user['username']}")
    return jsonify({'success': True})

# ================= Internal queue endpoint =================
@app.route('/internal/next-report/<role>', methods=['GET'])
def next_report(role):
    if role not in ('journalist', 'admin'):
        return jsonify({}), 400
    conn = get_db_connection()
    c = conn.cursor()
    row = c.execute('SELECT id, article_id FROM reports WHERE level = ? AND processed = 0 ORDER BY created_at ASC LIMIT 1', (role,)).fetchone()
    if not row:
        conn.close()
        return jsonify({})
    report_id, article_id = row
    c.execute('UPDATE reports SET processed = 1 WHERE id = ?', (report_id,))
    conn.commit()
    conn.close()
    return jsonify({'article_id': article_id})

@app.route('/api/articles/<int:article_id>/comments', methods=['POST'])
def add_article_comment(article_id):
    user = current_user_from_request()
    if not user:
        return jsonify({'error': 'unauthorized'}), 401

    data = request.get_json(silent=True) or {}
    content = bleach.clean((data.get('content') or '').strip())
    if not content:
        return jsonify({'error': 'empty'}), 400

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO comments (article_id, username, content) VALUES (?,?,?)',
              (article_id, user.get('username', 'user'), content))
    conn.commit()
    new_id = c.lastrowid
    row = c.execute('SELECT * FROM comments WHERE id = ?', (new_id,)).fetchone()
    conn.close()

    return jsonify({
        'id': row[0],
        'article_id': row[1],
        'username': row[2],
        'content': row[3],
        'created_at': row[4]
    }), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=PORT)
