from app import db


class User(db.Model):
    __table_name__ = 'user'

    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User('{self.id}', '{self.user_id}')>"
