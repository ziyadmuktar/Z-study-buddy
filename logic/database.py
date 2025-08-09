import sqlite3


def init_db():
    conn = sqlite3.connect("studybuddy.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            grade TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            hours REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(name, age, grade):
    conn = sqlite3.connect("studybuddy.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (name, age, grade) VALUES (?, ?, ?)", (name, age, grade))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return user_id

def insert_session(user_id, subject, hours):
    conn = sqlite3.connect("studybuddy.db")
    c = conn.cursor()
    c.execute("INSERT INTO sessions (user_id, subject, hours) VALUES (?, ?, ?)", (user_id, subject, hours))
    conn.commit()
    conn.close()
