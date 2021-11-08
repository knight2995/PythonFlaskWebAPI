import json

import werkzeug
from flask_restx import Resource, Namespace, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.service.photo_service import photo_service
from app.api.custom_exception.common_exception import ForbiddenException, NotExistPhoto, NotExistUser

photoNS = Namespace(
    name="photo",
    description="사진을 업로드 및 다운로드, 삭제 API",
)


@photoNS.route("/<int:photo_idx>")
@photoNS.response(200, 'Success')
@photoNS.response(403, 'Forbidden')
@photoNS.response(400, 'BadRequest')
@photoNS.response(500, 'Internal Error')
class Photo(Resource):

    @jwt_required()
    @photoNS.doc(security='apikey')
    def get(self, photo_idx):

        """ API: 사진 조회 API

        *JWT 가 필요합니다.
        photo_idx 에 해당하는 사진 데이터를 가져오는 API 입니다.
        photo_idx 는 GET /photos 를 통해 얻어올 수 있습니다.

        """

        try:
            image_data = photo_service.find_photo_data(photo_idx)
            return json.dumps({"imgData": image_data}), 200

        except NotExistUser as e:
            return json.dumps({'msg': str(e)}, ensure_ascii=False), 400

        except ForbiddenException as e:
            return json.dump({"msg": str(e)}, ensure_ascii=False), 403

        except Exception as e:
            return json.dump({"msg": str(e)}, ensure_ascii=False), 500

    @jwt_required()
    @photoNS.doc(security='apikey')
    def delete(self, photo_idx: int):

        """ API: 사진 삭제 API

        *JWT 가 필요합니다.
        photo_idx 에 해당하는 사진 데이터를 삭제하는 API 입니다.
        photo_idx 는 GET /photos 를 통해 얻어올 수 있습니다.
        삭제된 이미지는 실제 AWS S3에서 삭제됩니다.

        """

        try:
            photo_service.delete_photo_by_idx(photo_idx, get_jwt_identity())
            return json.dumps({"msg": "삭제 성공"}, ensure_ascii=False), 200

        except NotExistUser as e:
            return json.dumps({'msg': str(e)}, ensure_ascii=False), 400

        except ForbiddenException as e:
            return json.dumps({"msg": str(e)}, ensure_ascii=False), 403

        except NotExistPhoto as e:
            return json.dumps({"msg": str(e)}, ensure_ascii=False), 400

        except Exception as e:
            return json.dumps({"msg": str(e)}, ensure_ascii=False), 500


parser = reqparse.RequestParser()
parser.add_argument('file', location='files',
                    type=werkzeug.datastructures.FileStorage, required=True)


@photoNS.route("")
@photoNS.response(200, 'Success')
@photoNS.response(403, 'Forbidden')
@photoNS.response(500, 'Internal Error')
class Photos(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('file', location='files',
                             type=werkzeug.datastructures.FileStorage, required=True)
    post_parser.add_argument('album_idx', required=True, location='form')

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('album_idx', required=True)

    @jwt_required()
    @photoNS.expect(post_parser)
    @photoNS.doc(security='apikey')
    def post(self):

        """ API: 사진 업로드 API

        *JWT 가 필요합니다.
        album_idx 에 해당하는 앨범으로 사진 업로드하는 API 입니다.
        album_idx 는 GET /albums 를 통해 얻어올 수 있습니다.
        업로드한 이미지는 AWS S3 에 저장됩니다.

        """

        args = self.post_parser.parse_args()

        try:
            photo_service.photo_upload(get_jwt_identity(), args['file'], args['album_idx'])
            return json.dumps({"msg": '업로드 성공'}, ensure_ascii=False), 200

        except ForbiddenException as e:
            return json.dumps({"msg": str(e)}, ensure_ascii=False), 403

        except Exception as e:
            return json.dumps({"msg": str(e)}, ensure_ascii=False), 500

    @jwt_required()
    @photoNS.expect(get_parser)
    @photoNS.doc(security='apikey')
    def get(self):

        """ API: 사진 조회 API

        *JWT 가 필요합니다.
        album_idx 에 해당하는 앨범의 모든 사진 정보를 조회하는 API 입니다.
        album_idx 는 GET /albums 를 통해 얻어올 수 있습니다.
        여기서 얻은 idx 는 이미지 삭제 및 조회에 이용할 수 있습니다.

        """

        args = self.get_parser.parse_args()

        try:
            photos = photo_service.find_all_photos(args['album_idx'], get_jwt_identity())
            return json.dumps({"photos": photos}, ensure_ascii=False), 200

        except ForbiddenException as e:
            return json.dumps({"msg": str(e)}, ensure_ascii=False), 403

        except Exception as e:
            return json.dumps({"msg": str(e)}, ensure_ascii=False), 500



