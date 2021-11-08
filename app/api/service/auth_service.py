from app.api.model.user import User

from app.api.repository.user_repository import user_repository


class AuthService:

    # 로그인
    def login(self, user: User):

        find_user = user_repository.find_user_by_user_id(user.user_id)

        if find_user is None:
            return False

        if find_user.password == user.password:
            return find_user
        else:
            return False


auth_service = AuthService()
