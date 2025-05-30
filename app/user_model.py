from flask_login import UserMixin
from .database import get_db_connection


class User(UserMixin):
    def __init__(self, id, name, email, password_hash, role):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role

    def get_id(self):
        return str(self.id)
        
    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(row["id"], row["name"], row["email"], row["password_hash"], row["role"])
        return None
