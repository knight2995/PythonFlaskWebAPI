import base64
import hashlib
import json

import numpy as np
import werkzeug.datastructures
from cv2 import cv2

from app import s3

# 포토 업로드
from app.api.repository.album_repository import album_repository
from app.api.repository.photo_repository import photo_repository

from app.api.model.photo import Photo



def photo_upload(user_idx: int, file: werkzeug.datastructures.FileStorage, album_idx: int):

    # User 정보 가져오기

    # album_idx가 해당 User가 가지고 있는지 확인
    album = album_repository.find_album_by_album_idx(album_idx=album_idx)

    file_data = file.read()
    img_key = str(user_idx) + '_' + hashlib.md5(file_data).hexdigest()

    s3.put_object(Body=file_data, Bucket='knight2995-photo-album', Key=img_key)

    photo = Photo(file_name = file.filename, image_key= img_key, album = album)

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
    photos = photo_repository.find_photos_by_user_idx(album_idx)

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
