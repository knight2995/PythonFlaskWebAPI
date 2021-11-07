from app.api.model.user import User

from app import db


class UserRepository:

    def register_member(self, user: User):

        db.session.add(user)
        db.session.commit()

    def find_user_by_user_id(self, user_id: str):

        return User.query.filter_by(user_id=user_id).first()

    def find_user_by_user_idx(self, user_idx: int):

        return User.query.filter_by(idx=user_idx).first()

    def delete_user_by_user_idx(self, user_idx: int):

        db.session.delete(User.query.filter_by(idx=user_idx).first())
        db.session.commit()




user_repository = UserRepository()