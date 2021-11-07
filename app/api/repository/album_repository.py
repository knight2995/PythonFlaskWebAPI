from app.api.model.album import Album
from app import db


# user = User(id='1', username='김동현', email='악', password='2')
# album = Album(user=user, id = '2', username='테스트중')
# db.session.add(album)
# db.session.commit()


class AlbumRepository:

    def register_album(self, album: Album):
        db.session.add(album)
        db.session.commit()

    def find_albums_by_user_idx(self, user_idx: int):
        return Album.query.filter_by(user_idx=user_idx).all()

    def find_album_by_album_idx(self, album_idx: int):
        return Album.query.filter_by(idx=album_idx).first()

    def find_album_by_album_name(self, album_name: str):
        return Album.query.filter_by(album_name=album_name).first()

    def delete_album_by_album_idx(self, album_idx: int):
        db.session.delete(Album.query.filter_by(idx=album_idx).first())
        db.session.commit()


album_repository = AlbumRepository()
