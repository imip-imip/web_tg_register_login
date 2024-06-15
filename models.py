import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


def create_connection():
    conn = sqlite3.connect('users.db')
    return conn


def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                username TEXT NOT NULL UNIQUE, 
                password TEXT NOT NULL,
                anime TEXT NOT NULL,
                film TEXT NOT NULL)''')
    conn.commit()
    conn.close()


def insert_user(username, password, anime, film):
    conn = create_connection()
    c = conn.cursor()
    hashed_password = generate_password_hash(password)
    try:
        c.execute("INSERT INTO users (username, password, anime, film) VALUES (?, ?, ?, ?)",
                  (username, hashed_password, anime, film))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False


def get_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    if user and check_password_hash(user[2], password):
        return user
    return None


