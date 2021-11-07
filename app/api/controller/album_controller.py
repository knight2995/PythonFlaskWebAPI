from flask_restx import Resource, Namespace, reqparse

from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.service.album_service import register_album, find_all_albums, delete_album

from app.api.custom_exception.common_exception import AlbumDuplicatedException

albumNS = Namespace(
    name="album",
    description="앨범 정보",
)


@albumNS.route("/<int:album_idx>")
@albumNS.response(200, 'Success')
@albumNS.response(400, 'BadRequest')
@albumNS.response(500, 'Internal Error')
class Album(Resource):

    @jwt_required()
    @albumNS.doc(security='apikey')
    def delete(self, album_idx: int):

        """ API: 앨범 삭제
        album_idx 값에 해당하는 album 삭제
        """

        try:

            delete_album(album_idx, get_jwt_identity())
            return 'Success', 200

        except Exception as e:
            return str(e), 400


parser = reqparse.RequestParser()
parser.add_argument('album_name', required=True, help="앨범명")


@albumNS.route("")
@albumNS.response(200, 'Success')
@albumNS.response(409, 'Conflict Error')
@albumNS.response(500, 'Internal Error')
class Albums(Resource):

    @jwt_required()
    @albumNS.doc(security='apikey')
    @albumNS.expect(parser)
    def post(self):

        """ API: 앨범 추가 API
        상단의 Authorize 된 상태에서 가능
        """

        args = parser.parse_args()

        try:
            register_album(user_idx=get_jwt_identity(), album_name=args['album_name'])
            return 'Success', 200

        except AlbumDuplicatedException as e:
            return str(e), 409

        except Exception as e:
            return str(e), 500

    @jwt_required()
    @albumNS.doc(security='apikey')
    def get(self):

        """ API: 앨범 전체 조회
        현재 로그인 된 계정의 모든 앨범 정보를 조회
        idx 값은 사진 추가 및 앨범 삭제에 이용
        """

        return find_all_albums(get_jwt_identity()), 200
