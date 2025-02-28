import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS views 
                 (filename TEXT PRIMARY KEY, views INTEGER)''')
    conn.commit()
    conn.close()

def get_views(filename):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT views FROM views WHERE filename = ?", (filename,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def increment_views(filename):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    current_views = get_views(filename)
    if current_views == 0:
        c.execute("INSERT INTO views (filename, views) VALUES (?, 1)", (filename,))
    else:
        c.execute("UPDATE views SET views = views + 1 WHERE filename = ?", (filename,))
    conn.commit()
    conn.close()

def get_all_views():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT filename, views FROM views")
    result = dict(c.fetchall())
    conn.close()
    return result

def delete_views(filename):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("DELETE FROM views WHERE filename = ?", (filename,))
    conn.commit()
    conn.close()