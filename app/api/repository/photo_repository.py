from app.api.model.photo import Photo
from app import db


class PhotoRepository:

    def register_photo(self, photo: Photo):
        db.session.add(photo)
        db.session.commit()

    def find_photos_by_album_idx(self, album_idx: int):

        return Photo.query.filter_by(album_idx=album_idx).all()

    def find_photo_by_idx(self, photo_idx: int):

        return Photo.query.filter_by(idx=photo_idx).first()

    def delete_photo_by_idx(self, photo_idx: int):

        db.session.delete(Photo.query.filter_by(idx=photo_idx).first())
        db.session.commit()


photo_repository = PhotoRepository()
