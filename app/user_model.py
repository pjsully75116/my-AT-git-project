from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name, email, password_hash, role):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role

    def get_id(self):
        return str(self.id)
