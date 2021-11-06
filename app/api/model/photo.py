from app import db


class Photo(db.Model):
    __table_name__ = 'photo'

    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(300), nullable=False)

    image_key = db.Column(db.String(300), nullable=False)

    album_idx = db.Column(db.Integer, db.ForeignKey('album.idx',  ondelete='CASCADE'))
    album = db.relationship('Album', backref=db.backref('ref_album'))

    def __repr__(self):
        return f"<Photo('{self.id}', '{self.file_name}', '{self.image_key}')>"
