import sqlite3
from datetime import datetime



# Creating database
def create_db(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            chat_id INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            state TEXT NOT NULL,
            owner INTEGER,
            FOREIGN KEY(owner) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            user_id INTEGER NOT NULL,
            level_id INTEGER NOT NULL,
            result INTEGER NOT NULL,
            date TEXT NOT NULL,
            PRIMARY KEY (user_id, level_id),
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(level_id) REFERENCES levels(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            text TEXT NOT NULL,
            image_path TEXT
        )
    ''')

# Admin new device
def add_device(cursor, number, state):
    cursor.execute('''
        INSERT INTO devices (number, state, owner)
        VALUES (?, ?, NULL)
    ''', (number, state))

# Registration
def register_user(cursor, number, name, chat_id):
    cursor.execute("INSERT INTO users (name, chat_id) VALUES (?, ?)", (name, chat_id))
    user_id = cursor.lastrowid
    cursor.execute('''
        UPDATE devices
        SET owner = ?, state = ?
        WHERE number = ?
    ''', (user_id, 'active', number))

    if cursor.rowcount == 0:
        raise ValueError(f"Device with number {number} not found in database.")
    return user_id

def add_user_progress(cursor, user_id, level_id, result, date=None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT OR REPLACE INTO user_progress (user_id, level_id, result, date)
        VALUES (?, ?, ?, ?)
    ''', (user_id, level_id, result, date))

def add_level(cursor, name, text, image_path=None):
    cursor.execute('''
        INSERT INTO levels (name, text, image_path)
        VALUES (?, ?, ?)
    ''', (name, text, image_path))