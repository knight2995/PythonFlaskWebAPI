import json

from app.api.model.album import Album

from app.api.repository.photo_repository import photo_repository
from app.api.repository.user_repository import user_repository
from app.api.repository.album_repository import album_repository

from app.api.custom_exception.common_exception import NotExistAlbum, AlbumDuplicatedException, ForbiddenException

from app.api.service.photo_service import photo_service


class AlbumService:

    # 앨범 추가
    def register_album(self, user_idx: int, album_name: str):

        # user
        user = user_repository.find_user_by_user_idx(user_idx=user_idx)

        self.validate_duplicated_album_name(album_name, user_idx)

        album = Album(album_name=album_name, user=user)

        album_repository.register_album(album)

    # 앨범 이름 중복 체크
    def validate_duplicated_album_name(self, album_name: str, user_idx: int):

        if album_repository.find_album_by_album_name_and_user_idx(album_name, user_idx):
            raise AlbumDuplicatedException

    # 모든 앨범 조회
    def find_all_albums(self, user_idx: int):

        albums = album_repository.find_albums_by_user_idx(user_idx)

        # 직접 변환
        return list(map(lambda x: {'idx': x.idx, 'album_name': x.album_name}, albums))

    # 앨범 삭제
    def delete_album(self, album_idx: int, user_idx: int):

        # 앨범 존재 여부 체크
        album = album_repository.find_album_by_album_idx(album_idx)

        if album is None:
            raise NotExistAlbum

        # 앨범이 user 가 가지고 있는지 여부 확인
        if album.user_idx != user_idx:
            raise ForbiddenException

        # 앨범 내의 모든 사진을 삭제
        # 각 앨범마다 모든 사진 조회
        photos = list(photo_repository.find_photos_by_album_idx(album.idx))

        # s3에서 실제로 삭제
        photo_service.delete_photos_data(photos)

        # db 에서 삭제(cascade로 인해 자동으로 모두 삭제)
        album_repository.delete_album_by_album_idx(album.idx)


album_service = AlbumService()
