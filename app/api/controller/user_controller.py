import json

from flask_restx import Resource, Namespace, reqparse
from app.api.model.user import User

from app.api.service.user_service import user_service
from app.api.custom_exception.common_exception import UserDuplicatedException, NotExistUser

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

userNS = Namespace(
    name="user",
    description="User 추가, 삭제, 조회 API",
)

parser = reqparse.RequestParser()
parser.add_argument('id', required=True,  location='form')
parser.add_argument('password', required=True,  location='form')


# 회원가입
@userNS.route("")
@userNS.response(200, 'Success')
@userNS.response(409, 'Conflict')
@userNS.response(400, 'BadRequest')
@userNS.response(500, 'Internal Error')
class Users(Resource):

    # 회원 가입
    @userNS.expect(parser)
    def post(self):

        """ API: 회원가입 API

        id 와 password 를 입력하고 전송하면 확인할 수 있습니다.
        구현의 간단함을 위해 서버내에 어떠한 암호화 처리도 하지 않으므로 실제 비밀번호를 입력하지 말아주세요.
        validation 이 없어 100자 이하의 모든 문자열이 가능합니다.

        """

        args = parser.parse_args()

        user = User(user_id=args['id'], password=args['password'])

        try:
            user_service.register_user(user)
            return json.dumps({"msg": "회원 가입 성공"}, ensure_ascii=False), 200

        except UserDuplicatedException as e:
            return json.dumps({"msg": str(e)}, ensure_ascii=False), 409

        except Exception as e:
            return json.dumps({"msg": str(e)}, ensure_ascii=False), 500

    # 회원 조회
    @jwt_required()
    @userNS.doc(security='apikey')
    def get(self):

        """ API: User 정보 조회

        *JWT 가 필요합니다.
        Header 의 Authorization 필드 값에 JWT 를 이용해 JWT 토큰에 담긴 User별 고유값을 얻어오는 API 입니다.

        """

        user_idx = get_jwt_identity()

        try:
            user = user_service.find_user_by_idx(user_idx)
            return json.dumps({"user_idx": user_idx}, ensure_ascii=False), 200

        except NotExistUser as e:
            json.dumps({"msg": str(e)}, ensure_ascii=False), 400

        except Exception as e:
            return json.dumps({"msg": str(e)}, ensure_ascii=False), 500

    # 회원 삭제(탈퇴)
    @jwt_required()
    @userNS.doc(security='apikey')
    def delete(self):

        """ API: User 삭제

        *JWT 가 필요합니다.
        JWT 내의 값을 읽어 회원을 삭제하는 API입니다.

        """

        try:
            user_service.delete_user_by_idx(get_jwt_identity())
            return json.dumps({"msg": "삭제 성공"}, ensure_ascii=False), 200

        except NotExistUser as e:
            json.dumps({"msg": str(e)}, ensure_ascii=False), 400

        except Exception as e:
            json.dumps({"msg": str(e)}, ensure_ascii=False), 500
