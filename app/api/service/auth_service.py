from app.api.model import user
from app.api.repository.user_repository import user_repository


# 회원 가입
def check_id_pw(_user: user.User):
    # DAO 거치던가
    find_user = user_repository.find_user_by_user_id(_user.user_id)

    if find_user is None:
        return False

    if find_user.password == _user.password:
        return user
    else:
        return False

