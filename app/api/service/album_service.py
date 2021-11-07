import json

from app.api.model.album import Album
from app.api.repository.photo_repository import photo_repository
from app.api.repository.user_repository import user_repository
from app.api.repository.album_repository import album_repository

from app.api.custom_exception.common_exception import NotExistAlbum, AlbumDuplicatedException, ForbiddenException

from app.api.service.photo_service import delete_photo_data


# 앨범 추가
def register_album(user_idx: int, album_name: str):
    # user
    user = user_repository.find_user_by_user_idx(user_idx=user_idx)

    validate_duplicated_album_name(album_name)

    album = Album(album_name=album_name, user=user)

    album_repository.register_album(album)

    return True


# 중복 체크
def validate_duplicated_album_name(album_name: str):

    if album_repository.find_album_by_album_name(album_name):

        raise AlbumDuplicatedException


# 포토 다운로드
def find_all_albums(user_idx: int):
    # user = user_repository.find_user_by_user_idx(user_idx)
    albums = album_repository.find_albums_by_user_idx(user_idx)

    # 직접 변환
    temp = list(map(lambda x: {'idx': x.idx, 'album_name': x.album_name}, albums))
    return json.dumps({"albums": temp})


# 앨범 삭제
def delete_album(album_idx: int, user_idx: int):

    # 앨범 존재 여부 체크
    album = album_repository.find_album_by_album_idx(album_idx)

    if album is None:
        raise NotExistAlbum

    # 앨범이 user 가 가지고 있는지 여부 확인
    if album.user_idx != user_idx:
        raise ForbiddenException

    # 각 앨범마다 모든 사진 조회
    photos = list(photo_repository.find_photos_by_album_idx(album.idx))
    # s3에서 삭제
    delete_photo_data(photos)

    album_repository.delete_album_by_album_idx(album.idx)
