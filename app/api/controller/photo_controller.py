import werkzeug
from flask_restx import Resource, Namespace, reqparse

from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.service.photo_service import photo_upload, photo_download, find_all_photos, find_photo_data

from app.api.custom_exception.common_exception import ForbiddenException

photoNS = Namespace(
    name="photo",
    description="사진을 올리고 다운로드 하고 보는 컨트롤러",
)


@photoNS.route("/<int:photo_idx>")
@photoNS.response(200, 'Success')
@photoNS.response(403, 'Forbidden')
@photoNS.response(500, 'Internal Error')
class Photo(Resource):

    @jwt_required()
    def get(self, photo_idx):

        try:
            ret = find_photo_data(photo_idx)
            return ret, 200

        except ForbiddenException as e:
            return str(e), 403

        except Exception as e:
            return '', 500


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
    post_parser.add_argument('album_idx', required=True)

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('file', location='files',
                             type=werkzeug.datastructures.FileStorage, required=True)
    get_parser.add_argument('album_idx', required=True)

    @jwt_required()
    @photoNS.expect(post_parser)
    def post(self):

        args = self.post_parser.parse_args()

        photo_upload(get_jwt_identity(), args['file'], args['album_idx'])

        return 'ok', 200

    @jwt_required()
    @photoNS.expect(get_parser)
    def get(self):

        args = parser.parse_args()

        return find_all_photos(args['album_idx']), 200
