import sqlite3

class Posts:
    def __init__(self, sno, title, slug, content, date, img_file):
        self.sno = sno
        self.title = title
        self.slug = slug
        self.content = content
        self.date = date
        self.img_file = img_file

def connect_to_database():
    return sqlite3.connect('your_database.db')

def create_table():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            sno INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            slug TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT,
            img_file TEXT
        )
    ''')
    connection.commit()
    connection.close()

def insert_post(title, slug, content, date, img_file):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO posts (title, slug, content, date, img_file)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, slug, content, date, img_file))
    connection.commit()
    connection.close()

def get_all_posts():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM posts')
    posts = []
    for row in cursor.fetchall():
        post = Posts(row[0], row[1], row[2], row[3], row[4], row[5])
        posts.append(post)
    connection.close()
    return posts
