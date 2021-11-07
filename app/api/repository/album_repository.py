from app.api.model.album import Album

from app import db


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

    def find_album_by_album_name_and_user_idx(self, album_name: str, user_idx: int):
        return Album.query.filter_by(album_name=album_name, user_idx=user_idx).first()


album_repository = AlbumRepository()
