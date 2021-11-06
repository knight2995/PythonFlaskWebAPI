from app import db


class Album(db.Model):
    __table_name__ = 'photo'

    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    album_name = db.Column(db.String(100), nullable=False)

    user_idx = db.Column(db.Integer, db.ForeignKey('user.idx',  ondelete='CASCADE'))
    user = db.relationship('User', backref=db.backref('ref_user'))

    def __repr__(self):
        return f"<Album('{self.idx}', '{self.album_name}')>"
