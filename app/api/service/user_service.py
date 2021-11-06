from app.api.model import user
from app.api.repository.user_repository import user_repository
# 회원 가입
def register_member(_user : user.User):

    # DAO 거치던가
    user_repository.register_member(_user)
    return _user