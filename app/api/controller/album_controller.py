import json

from flask_restx import Resource, Namespace, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.service.album_service import album_service
from app.api.custom_exception.common_exception import AlbumDuplicatedException, NotExistAlbum

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

        *JWT 가 필요합니다.
        album_idx 값에 해당하는 album 을 삭제하는 API 입니다.
        album_idx 는 GET /albums 을 이용해 얻어올 수 있습니다.

        """

        try:
            album_service.delete_album(album_idx, get_jwt_identity())
            return json.dumps({'msg': '앨범 삭제 성공'}, ensure_ascii=False), 200

        except NotExistAlbum as e:
            json.dumps({"msg": str(e)}, ensure_ascii=False), 400

        except Exception as e:
            return json.dumps({'msg': str(e)}, ensure_ascii=False), 500


parser = reqparse.RequestParser()
parser.add_argument('album_name', required=True, help="앨범명", location='form')


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

        *JWT 가 필요합니다.
        현재 로그인된 계정에 앨범을 추가하는 API 입니다.

        """

        args = parser.parse_args()

        try:
            album_service.register_album(user_idx=get_jwt_identity(), album_name=args['album_name'])
            return json.dumps({'msg': '앨범 추가 성공'}, ensure_ascii=False), 200

        except AlbumDuplicatedException as e:
            return json.dumps({'msg': str(e)}, ensure_ascii=False), 409

        except Exception as e:
            return json.dumps({'msg': str(e)}, ensure_ascii=False), 500

    @jwt_required()
    @albumNS.doc(security='apikey')
    def get(self):

        """ API: 앨범 전체 조회

        *JWT 가 필요합니다.
        현재 로그인된 계정의 모든 앨범 정보를 조회하는 API 입니다.
        여기서 조회한 idx 값을 이용해서 사진 추가 및 앨범 삭제에 이용할 수 있습니다.

        """

        albums = album_service.find_all_albums(get_jwt_identity())

        return json.dumps({"albums": albums}, ensure_ascii=False), 200
