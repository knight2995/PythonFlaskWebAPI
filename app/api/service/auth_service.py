from app.api.model.user import User
from app.api.repository.user_repository import user_repository


# 회원 가입
def check_id_pw(user: User):
    # DAO 거치던가
    find_user = user_repository.find_user_by_user_id(user.user_id)

    if find_user is None:
        return False

    if find_user.password == user.password:
        return find_user
    else:
        return False

