from app.api.model.user import User

from app.api.repository.user_repository import user_repository
from app.api.repository.album_repository import album_repository
from app.api.repository.photo_repository import photo_repository

from app.api.service.photo_service import photo_service

from app.api.custom_exception.common_exception import UserDuplicatedException, ForbiddenException, NotExistUser


class UserService:

    # 회원 가입
    def register_user(self, user: User):
        # 회원 중복체크
        self.validate_duplicated_user(user)

        user_repository.register_member(user)

        return user

    # User id 중복 체크
    def validate_duplicated_user(self, user: User):
        if user_repository.find_user_by_user_id(user.user_id):
            raise UserDuplicatedException

    # 회원 조회
    def find_user_by_idx(self, user_idx: int):
        # 실제 존재하는 지 확인 <Not implemented>
        user = user_repository.find_user_by_user_idx(user_idx)
        return user

    # 회원 삭제
    def delete_user_by_idx(self, user_idx: int):

        # 존재하는 회원인지 확인
        user = user_repository.find_user_by_user_idx(user_idx)

        if user is None:
            raise NotExistUser

        # 회원을 삭제함으로써 회원이 가졌던 모든 앨범과 그 사진들 삭제

        # 1. Album list 조회
        albums = album_repository.find_albums_by_user_idx(user_idx)

        # 2. 각 앨범마다 모든 사진 조회
        photos = sum(list(map(lambda album: photo_repository.find_photos_by_album_idx(album.idx), albums)), [])
        # 3. s3에서 삭제
        photo_service.delete_photos_data(photos)

        # 회원 삭제(cascade 로 DB 상에서 앨범과 사진은 자동으로 삭제)
        user_repository.delete_user_by_user_idx(user_idx)


user_service = UserService()
