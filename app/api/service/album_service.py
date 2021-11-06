import json

from app.api.model.album import Album
from app.api.repository.user_repository import user_repository
from app.api.repository.album_repository import album_repository


# 앨범 추가
def register_album(user_idx: int, album_name: str):

    user = user_repository.find_user_by_user_idx(user_idx=user_idx)

    album = Album(album_name=album_name, user=user)

    album_repository.register_album(album)

    return True


# 포토 다운로드
def find_all_albums(user_idx: int):

    # user = user_repository.find_user_by_user_idx(user_idx)
    albums = album_repository.find_albums_by_user_idx(user_idx)

    # 직접 변환
    temp = list(map(lambda x: {'idx': x.idx, 'album_name' : x.album_name}, albums))
    return json.dumps({"albums": temp})

