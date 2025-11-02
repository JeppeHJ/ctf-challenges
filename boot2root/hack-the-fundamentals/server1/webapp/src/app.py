from flask import Flask, render_template, request, redirect, url_for, flash, session
import logging
import os
import datetime
import sqlite3
from db_setup import create_database
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app with correct template folder
app = Flask(__name__, 
            template_folder='/opt/webapp/templates',
            static_folder='/opt/webapp/static')

# Set a secret key for sessions and flash messages
app.secret_key = 'eaaa_lab_server_secret_key'

# Initialize database
db_path = create_database()

# Configure upload folder - deliberately in a public web location (security vulnerability)
UPLOAD_FOLDER = '/opt/webapp/static/img'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure allowed extensions (deliberately vulnerable)
ALLOWED_EXTENSIONS = {
    # Web shells
    'php', 'php3', 'php4', 'php5', 'php7', 'phtml', 'phar',
    # ASP/ASPX shells
    'asp', 'aspx', 'config', 'ashx', 'asmx', 'aspq', 'axd',
    # JSP shells
    'jsp', 'jspx', 'jsw', 'jsv', 'jspf',
    # CGI and other shells
    'cgi', 'pl', 'py', 'rb', 'sh', 'bash', 'exe', 'dll', 'so',
    # Web archive formats that can contain shells
    'war', 'jar',
    # Standard image formats (for legitimate use)
    'png', 'jpg', 'jpeg', 'gif'
}

def get_db_connection():
    """Get a connection to the SQLite database"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def authenticate_user(username, password):
    """Authenticate a user against the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query the database for the user
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            return True, dict(user)
        else:
            return False, None
            
    except Exception as e:
        logger.error(f"Database error during authentication: {str(e)}")
        return False, None

def get_profile_image(username):
    """Get the profile image for a user"""
    try:
        files = [f for f in os.listdir(UPLOAD_FOLDER) if f != 'todo.txt']
        if files:
            # Get the most recent file
            latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(UPLOAD_FOLDER, f)))
            return f"/static/img/{latest_file}"
    except Exception as e:
        logger.error(f"Error getting profile image: {str(e)}")
    
    # Return default if no uploads found
    return "/static/img/profile_picture.png"

def allowed_file(filename):
    """Check if a file has an allowed extension (DELIBERATELY VULNERABLE)"""
    # Get the extension
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    # VULNERABLE: This only checks the extension, not the actual file content
    # Also, it allows dangerous extensions like .php and .aspx
    return ext in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Log the login attempt (for demo purposes)
        logger.info(f"Login attempt - Username: {username}")
        
        # Authenticate against the database
        is_valid, user_data = authenticate_user(username, password)
        
        if is_valid:
            # Set session variables for the logged in user
            session['logged_in'] = True
            session['username'] = username
            session['role'] = user_data['role']
            
            # Redirect to profile page on successful login
            flash('Login successful!', 'info')
            return redirect(url_for('profile'))
        else:
            # Flash error message on failed login
            flash('Invalid credentials. Please try again.', 'error')
            return render_template('login.html', error=True)
    
    # If it's a GET request, just show the login form
    return render_template('login.html', error=False)

@app.route('/profile')
def profile():
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    
    # Get user information
    username = session.get('username')
    role = session.get('role', 'User')
    
    # Get current year for footer
    now = datetime.datetime.now()
    
    # Get profile image
    profile_image = get_profile_image(username)
    
    return render_template('profile.html', username=username, role=role, now=now, profile_image=profile_image)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('profile'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('profile'))

    if file:
        # VULNERABLE: Keep original filename and make executable
        # This allows attackers to control the exact URL of their shell
        filename = secure_filename(file.filename)  # Basic sanitation but still vulnerable
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        # Make file executable for maximum vulnerability
        os.chmod(file_path, 0o777)
        logger.info(f"File uploaded: {filename}")
        
    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    # Clear session data
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Run in production mode without debugger
    app.debug = False
    app.run(host='0.0.0.0', port=5000) 