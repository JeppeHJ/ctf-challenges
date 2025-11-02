import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

JOURNALIST_EMAIL = '0xjeppe@cakenews.ctf'
JOURNALIST_PASSWORD = os.environ.get('JOURNALIST_PASSWORD')

ADMIN_EMAIL = 'admin@brunnerne.ctf'
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

FLAG = os.environ.get('FLAG')

def get_db_connection():
    return sqlite3.connect('brunnernelogin.db')

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    hashed_admin_pw = generate_password_hash(ADMIN_PASSWORD)
    hashed_journalist_pw = generate_password_hash(JOURNALIST_PASSWORD)
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            flag TEXT
        )
    ''')
    
    c.execute('''
        INSERT OR IGNORE INTO users (email, password, flag) 
        VALUES (?, ?, ?)
    ''', (ADMIN_EMAIL, hashed_admin_pw, FLAG))
 
    c.execute('''
        INSERT OR IGNORE INTO users (email, password)
        VALUES (?, ?)
    ''', (JOURNALIST_EMAIL, hashed_journalist_pw))
    
    conn.commit()
    conn.close()

def get_user_by_credentials(email, password):
    conn = get_db_connection()
    c = conn.cursor()
    row = c.execute(
        'SELECT * FROM users WHERE email = ?',
        (email,)
    ).fetchone()
    conn.close()
    if row and check_password_hash(row[2], password):
        return row
    return None

def create_user(email, password):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        hashed_pw = generate_password_hash(password)
        c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
