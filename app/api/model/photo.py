from app import db


# Photo Class
class Photo(db.Model):
    __table_name__ = 'photo'

    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(300), nullable=False)

    image_key = db.Column(db.String(300), nullable=False)

    album_idx = db.Column(db.Integer, db.ForeignKey('album.idx', ondelete='CASCADE'))
    album = db.relationship('Album', backref=db.backref('ref_album', cascade='all, delete-orphan'))

    def __repr__(self):
        return f"<Photo('{self.idx}', '{self.file_name}', '{self.image_key}')>"
