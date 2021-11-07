from flask_restx import Resource, Namespace, reqparse

from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.service.album_service import register_album, find_all_albums


albumNS = Namespace(
    name="album",
    description="앨범 정보",
)

parser = reqparse.RequestParser()
parser.add_argument('album_name', required=True)

@albumNS.route("")
class Albums(Resource):

    @jwt_required()
    @albumNS.expect(parser)
    def post(self):

        args = parser.parse_args()

        register_album(user_idx=get_jwt_identity(), album_name=args['album_name'])

        return 'ok', 200

    @jwt_required()
    def get(self):

        return find_all_albums(get_jwt_identity()), 200





