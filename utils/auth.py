from flask_login import UserMixin
from utils.db import get_db

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

def get_user_by_id(user_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if row:
        return User(row['id'], row['username'])
    return None

def get_user_by_username(username):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row
