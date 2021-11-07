from app.api.model import photo
from app import db


# user = User(id='1', username='김동현', email='악', password='2')
# album = Album(user=user, id = '2', username='테스트중')
# db.session.add(album)
# db.session.commit()



class PhotoRepository:

    def register_photo(self, _photo: photo.Photo):
        db.session.add(_photo)
        db.session.commit()

    def find_photos_by_album_idx(self, album_idx: int):

        return photo.Photo.query.filter_by(album_idx=album_idx).all()

    def find_photo_by_idx(self, photo_idx: int):

        return photo.Photo.query.filter_by(idx=photo_idx).first()


photo_repository = PhotoRepository()
