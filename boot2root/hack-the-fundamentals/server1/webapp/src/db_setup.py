import sqlite3
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database():
    """Create the SQLite database and initialize it with data from secret.txt"""
    
    # Define database path
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db'))
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Connect to the database (will create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')
    
    # Read credentials from secret.txt
    try:
        # Path to secret.txt in FTP directory
        secret_file = '/srv/ftp/secret.txt'
        with open(secret_file, 'r') as f:
            lines = f.readlines()
            
        if len(lines) >= 2:
            username = lines[0].strip()
            password = lines[1].strip()
            
            # Check if user already exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
            exists = cursor.fetchone()[0]
            
            if not exists:
                # Insert the admin user
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, password, 'admin')
                )
                logger.info(f"Added user '{username}' to database")
            else:
                logger.info(f"User '{username}' already exists in database")
                
        else:
            logger.error("Invalid format in secret.txt")
    except Exception as e:
        logger.error(f"Error reading credentials from secret.txt: {str(e)}")
        # Add a default user if we couldn't read from secret.txt
        cursor.execute(
            "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
            ('hans@eaaa.dk', 'kBaqIR2Bkle%YZnZq5hK', 'admin')
        )
        logger.info("Added default user to database")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    logger.info(f"Database initialized at {db_path}")
    return db_path

if __name__ == "__main__":
    create_database() 