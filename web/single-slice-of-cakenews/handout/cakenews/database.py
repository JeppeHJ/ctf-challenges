import sqlite3
import os

JOURNALIST_EMAIL = '0xjeppe@cakenews.ctf'
JOURNALIST_PASSWORD = os.environ.get('JOURNALIST_PASSWORD')

ADMIN_EMAIL = 'admin@brunnerne.ctf'
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

def init_db():
    conn = sqlite3.connect('cakenews.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT DEFAULT 'NEWS',
            image_url TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER,
            username TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (article_id) REFERENCES articles (id)
        )
    ''')

    # Queue table for journalist/admin reports
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL,
            level TEXT NOT NULL, -- "journalist" or "admin"
            processed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (article_id) REFERENCES articles (id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    if not c.execute('SELECT * FROM articles').fetchone():
        sample_articles = [
            ('LIVE: CyberSkills cake-competition', 'Watch the most talented bakers compete for the ultimate chocolate cake crown in this thrilling live competition.', '0xjeppe', 'LIVE', '/static/images/featured-cake.jpg'),
            ('Othello is absolute garbage', 'Once considered a classic, the Othello cake is now being dragged through the frosting for its bland flavor, dry texture, and confused identity. Is it time we stop pretending this relic is edible?', '0xjeppe', 'RECIPES', '/static/images/othello.jpg'),
            ('Kalmarunionen caught baking a cake with a file in it', 'Baking community is stunned over recent discoveries that the members of Kalmarunionen have been baking cakes with files in them.', '0xjeppe', 'DEBATE', '/static/images/cheesecake.jpg'),
            ('0-Day Aarhus ranked #2 in Denmark on BakeTime - how?', 'Steadily ranked #4 in Denmark, they have all of a sudden risen to the top of the rankings.', '0xjeppe', 'BUSINESS', '/static/images/cupcake.jpg'),
            ('Insane: Jutlandia-members thought cheesecake was made of cheese', 'In a stunning revelation, it has been discovered that the members of Jutlandia have been baking cheesecake with cheese.', '0xjeppe', 'INNOVATION', '/static/images/birthday-cake.jpg'),
            ('Pwnies invent new caketech: Cake with unicorn meat', 'Revolutionary new technology has allowed Pwnies to create a cake comprised of 100% unicorn meat.', '0xjeppe', 'TRENDS', '/static/images/wedding-cake.jpg')
        ]

        for title, content, author, category, image_url in sample_articles:
            c.execute('''
                INSERT INTO articles (title, content, author, category, image_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, content, author, category, image_url))

        sample_comments = [
            (1, 'JensMyrup', 'This championship is absolutely amazing! The talent is incredible.'),
            (1, 'Linda', 'I can\'t believe how perfect that chocolate ganache looks!'),
            (2, 'BrunnerSpy', 'Othello gave me SARS'),
            (3, 'Killerdog', 'This is how we encrypt our data!'),
            (4, 'Nissen', 'How did we let this happen in Brunnerne?'),
            (5, 'c3lphie', 'I reverse engineered the cake and it was 100% cheese')
        ]

        for article_id, username, content in sample_comments:
            c.execute('''
                INSERT INTO comments (article_id, username, content)
                VALUES (?, ?, ?)
            ''', (article_id, username, content))

    c.executemany("""
        INSERT OR IGNORE INTO users (email, username, role)
        VALUES (?, ?, ?)
    """, [
        (ADMIN_EMAIL, 'BrunnerneAdmin', 'admin'),
        (JOURNALIST_EMAIL, '0xjeppe', 'journalist')
    ])

    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('cakenews.db')
