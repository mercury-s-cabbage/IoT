import sqlite3
from datetime import datetime



# Creating database
def create_db(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL UNIQUE,
            state TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            chat_id INTEGER NOT NULL,
            device_id INTEGER,
            FOREIGN KEY(device_id) REFERENCES devices(id)
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
            image_path TEXT,
            answer INTEGER,
            loose_text TEXT
        )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                data INTEGER NOT NULL
            )
        ''')

# Admin new device
def add_device(cursor, number, state):
    cursor.execute('''
        INSERT INTO devices (number, state)
        VALUES (?, ?)
    ''', (number, state))


def register_user(cursor, name, chat_id, device_number):
    cursor.execute('SELECT id FROM devices WHERE number = ?', (device_number,))
    device = cursor.fetchone()

    if device is None:
        raise ValueError(f"Устройство с номером {device_number} не найдено в базе данных.")

    device_id = device[0]

    cursor.execute('''
        INSERT INTO users (name, chat_id, device_id)
        VALUES (?, ?, ?)
    ''', (name, chat_id, device_id))

    user_id = cursor.lastrowid

    cursor.execute('''
        UPDATE devices
        SET state = ?
        WHERE id = ?
    ''', ('active', device_id))

    return user_id

def add_user_progress(cursor, user_id, level_id, result, date=None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT OR REPLACE INTO user_progress (user_id, level_id, result, date)
        VALUES (?, ?, ?, ?)
    ''', (user_id, level_id, result, date))

def add_level(cursor, name, text, answer, loose_test, image_path=None):
    if not (1000 <= answer <= 9999):
        raise ValueError("Answer должен быть четырёхзначным числом от 1000 до 9999")

    cursor.execute('''
        INSERT INTO levels (name, text, image_path, answer, loose_text)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, text, image_path, answer, loose_test))
