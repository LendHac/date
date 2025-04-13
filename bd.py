import sqlite3

def db_connect():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id AUTO_INCREMENT,
                        chat_id INTEGER NOT NULL,
                        course INTEGER NOT NULL,
                        group_name TEXT NOT NULL)''')
    conn.commit()
    return conn
db_connect()

def data_set(chat_id, course, group_name):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (chat_id, course, group_name)
        VALUES (?, ?, ?)
    ''', (chat_id, course, group_name))
    conn.commit()
    conn.close()