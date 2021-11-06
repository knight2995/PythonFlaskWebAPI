from app.api.model import album
from app import db


# user = User(id='1', username='김동현', email='악', password='2')
# album = Album(user=user, id = '2', username='테스트중')
# db.session.add(album)
# db.session.commit()


class AlbumRepository:

    def register_album(self, _album: album.Album):
        db.session.add(_album)
        db.session.commit()

    def find_albums_by_user_idx(self, user_idx: int):
        # albums = album.Album.objects.filter(user_idx=user_idx)
        return album.Album.query.filter_by(user_idx=user_idx).all()
        # user.User.query.filter_by(user_id = user_id).first()

    def find_album_by_album_idx(self, album_idx: int):
        return album.Album.query.filter_by(idx=album_idx).first()


album_repository = AlbumRepository()
