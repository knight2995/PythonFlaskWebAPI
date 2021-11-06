import werkzeug
from flask_restx import Resource, Namespace, reqparse

from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.service.photo_service import photo_upload, photo_download, find_all_photos, find_photo_data


photoNS = Namespace(
    name="photo",
    description="사진을 올리고 다운로드 하고 보는 컨트롤러",
)


@photoNS.route("/<int:idx>")
class Photo(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', location='files',
                            type=werkzeug.datastructures.FileStorage, required=True)

        args = parser.parse_args()

        photo_upload(get_jwt_identity(), args['file'])

        return 'ok', 200

    @jwt_required()
    def get(self, idx):

        ret = find_photo_data(idx)
        return ret, 200


@photoNS.route("")
class Photos(Resource):

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', location='files',
                            type=werkzeug.datastructures.FileStorage, required=True)
        parser.add_argument('album_idx', required=True)

        args = parser.parse_args()

        photo_upload(get_jwt_identity(), args['file'], args['album_idx'])

        return 'ok', 200

    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('album_idx', required=True)

        args = parser.parse_args()

        return find_all_photos(args['album_idx']), 200









