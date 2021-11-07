from app.api.model.user import User
from app.api.repository.user_repository import user_repository
from app.api.custom_exception.common_exception import UserDuplicatedException


# 회원 가입
def register_user(user: User):

    # 회원 중복체크
    validate_duplicated_user(user)

    user_repository.register_member(user)

    return user


def validate_duplicated_user(user: User):

    if user_repository.find_user_by_user_id(user.user_id):
        raise UserDuplicatedException
