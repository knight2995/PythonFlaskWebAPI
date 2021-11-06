from app.api.model import user
from app import db

# user = User(id='1', username='김동현', email='악', password='2')
# album = Album(user=user, id = '2', username='테스트중')
# db.session.add(album)
# db.session.commit()

class UserRepository:

    def register_member(self, _user: user.User):

        db.session.add(_user)
        db.session.commit()

    def find_user_by_user_id(self, user_id: str):

        return user.User.query.filter_by(user_id=user_id).first()

    def find_user_by_user_idx(self, user_idx: int):

        return user.User.query.filter_by(idx=user_idx).first()


user_repository = UserRepository()