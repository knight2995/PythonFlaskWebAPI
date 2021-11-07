import base64
import hashlib
import json
from datetime import datetime

import numpy as np
import werkzeug.datastructures
from cv2 import cv2

from app import s3

# 포토 업로드
from app.api.repository.album_repository import album_repository
from app.api.repository.photo_repository import photo_repository

from app.api.model.photo import Photo

from app.api.custom_exception.common_exception import ForbiddenException


def photo_upload(user_idx: int, file: werkzeug.datastructures.FileStorage, album_idx: int):
    album = album_repository.find_album_by_album_idx(album_idx=album_idx)

    # album_idx 를 해당 User 가 가지고 있는지 확인
    if album.user_idx != user_idx:
        raise ForbiddenException

    file_data = file.read()

    dt_obj = datetime.now()
    millisec = dt_obj.timestamp() * 1000

    img_key = str(user_idx) + '_' + str(millisec) + '_' + hashlib.md5(file_data).hexdigest()

    s3.put_object(Body=file_data, Bucket='knight2995-photo-album', Key=img_key)

    photo = Photo(file_name=file.filename, image_key=img_key, album=album)

    photo_repository.register_photo(photo)

    return True


# 포토 다운로드
def photo_download(key: str):
    data = s3.get_object(Bucket='knight2995-photo-album', Key=key).get('Body').read()
    img = cv2.imdecode(np.fromstring(data, np.uint8), cv2.IMREAD_UNCHANGED)

    _, buffer = cv2.imencode('.jpg', img)

    return json.dumps({"imgData": base64.b64encode(buffer).decode('utf-8')})


# 모든 사진 조회(앨범 내의)
def find_all_photos(album_idx: int):
    photos = photo_repository.find_photos_by_album_idx(album_idx)

    # 직접 변환
    temp = list(map(lambda x: {'idx': x.idx, 'image_key': x.image_key}, photos))
    return json.dumps({"photos": temp})


# idx에 해당하는 사진 조회 후 반환
def find_photo_data(idx: int):
    photo = photo_repository.find_photo_by_idx(photo_idx=idx)

    data = s3.get_object(Bucket='knight2995-photo-album', Key=photo.image_key).get('Body').read()
    img = cv2.imdecode(np.fromstring(data, np.uint8), cv2.IMREAD_UNCHANGED)

    _, buffer = cv2.imencode('.jpg', img)

    return json.dumps({"imgData": base64.b64encode(buffer).decode('utf-8')})


def delete_photo(photo_idx: int):

    """ Todo 검증 코드 필요함 """
    delete_photo_data([photo_repository.find_photo_by_idx(photo_idx)])
    photo_repository.delete_photo_by_idx(photo_idx)


# s3에서 삭제
def delete_photo_data(photos: list):
    for photo in photos:
        s3.delete_object(Bucket='knight2995-photo-album', Key=photo.image_key)
