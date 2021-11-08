import base64
import hashlib
import json
from datetime import datetime

import numpy as np
import werkzeug.datastructures
from cv2 import cv2

from app import s3
from app.api.custom_exception.common_exception import ForbiddenException, NotExistPhoto, NotExistAlbum, NotExistUser
from app.api.model.photo import Photo
# 포토 업로드
from app.api.repository.album_repository import album_repository
from app.api.repository.photo_repository import photo_repository
from app.api.repository.user_repository import user_repository


class PhotoService:

    # 사진 업로드
    def photo_upload(self, user_idx: int, file: werkzeug.datastructures.FileStorage, album_idx: int):

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

    # 사진 다운로드
    def photo_download(self, key: str):

        data = s3.get_object(Bucket='knight2995-photo-album', Key=key).get('Body').read()
        img = cv2.imdecode(np.fromstring(data, np.uint8), cv2.IMREAD_UNCHANGED)

        _, buffer = cv2.imencode('.jpg', img)

        return json.dumps({"imgData": base64.b64encode(buffer).decode('utf-8')})

    # 모든 사진 조회(앨범 내의)
    def find_all_photos(self, album_idx: int, user_idx: int):

        # user 존재 여부 체크
        user = user_repository.find_user_by_user_idx(user_idx=user_idx)

        if user is None:
            raise NotExistUser

        # 앨범이 존재하는 지 여부 확인
        album = album_repository.find_album_by_album_idx(album_idx)

        if album is None:
            raise NotExistAlbum

        # album_idx 를 User 가 가지고 있는지 확인
        if album.user_idx != user_idx:
            raise ForbiddenException

        photos = photo_repository.find_photos_by_album_idx(album_idx)

        # 직접 변환
        photos_data = list(map(lambda photo: {'idx': photo.idx, 'image_key': photo.image_key}, photos))
        return photos_data

    # idx 에 해당하는 사진 조회 후 이미지 데이터 반환
    def find_photo_data(self, idx: int):

        photo = photo_repository.find_photo_by_idx(photo_idx=idx)

        data = s3.get_object(Bucket='knight2995-photo-album', Key=photo.image_key).get('Body').read()
        img = cv2.imdecode(np.fromstring(data, np.uint8), cv2.IMREAD_UNCHANGED)

        _, buffer = cv2.imencode('.jpg', img)

        return base64.b64encode(buffer).decode('utf-8')

    # s3에서 실제 이미지 삭제
    def delete_photo(self, image_key):

        s3.delete_object(Bucket='knight2995-photo-album', Key=image_key)

    # photo_idx 에 해당하는 이미지 삭제
    def delete_photo_by_idx(self, photo_idx: int, user_idx: int):

        # user 존재 여부 체크
        user = user_repository.find_user_by_user_idx(user_idx=user_idx)

        if user is None:
            raise NotExistUser

        # 사진의 존재 여부 확인
        photo = photo_repository.find_photo_by_idx(photo_idx)

        if photo is None:
            raise NotExistPhoto

        # 현재 user 가 가진 앨범 안에 존재하는 사진 여부 확인
        albums = album_repository.find_albums_by_user_idx(user_idx)
        album_idx_list = list(map(lambda album: album.idx, albums))

        if photo.album_idx not in album_idx_list:
            raise ForbiddenException

        self.delete_photo(photo_repository.find_photo_by_idx(photo_idx).image_key)
        photo_repository.delete_photo_by_idx(photo_idx)

    # 사진 리스트 단위 삭제
    def delete_photos_data(self, photos: list):

        for photo in photos:
            self.delete_photo(photo.image_key)


photo_service = PhotoService()
