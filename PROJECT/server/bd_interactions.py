import sqlite3

conn = sqlite3.connect('DungeonGame.db')
cursor = conn.cursor()

def add_user(chat_id, device_id, name):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            chat_id INTEGER,
            device_id INTEGER
        )
    ''')

    cursor.execute(f"INSERT INTO users (name, chat_id, device_id) VALUES (?, ?, ?)",
                   (name, chat_id, device_id))
    conn.commit()

def add_historical(time, data):
    pass

#TODO: таблица пользователей, табл с историческими данными пользователей,
# табл задач для игры, табл результатов пользователей