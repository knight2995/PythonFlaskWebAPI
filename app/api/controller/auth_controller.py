import json

from flask_jwt_extended import create_access_token
from flask_restx import Resource, Namespace, reqparse

from app.api.model.user import User
from app.api.service.auth_service import auth_service

authNS = Namespace(
    name="auth",
    description="로그인 인증(JWT)",
)

parser = reqparse.RequestParser()
parser.add_argument('id', location='form', required=True)
parser.add_argument('password', location='form', required=True)


@authNS.route("/login")
@authNS.response(200, 'Success')
@authNS.response(401, 'Login Error')
@authNS.response(500, 'Internal Error')
class Login(Resource):

    @authNS.expect(parser)
    def post(self):

        """ API: 로그인 API

        id, password 를 이용해서 로그인하는 API입니다.
        실행 시 token 값을 얻을 수 있고 이를 이용해 다른 API의 인증에 사용됩니다.
        웹페이지 상단의 Authorize 를 눌러 JWT 를 입력하면 사용하실 수 있습니다.

        """

        args = parser.parse_args()

        # User 객체 생성
        user = User(user_id=args['id'], password=args['password'])

        # 넘어온 id, password 로 해당 User 조회
        try:
            find_user = auth_service.login(user)

            if find_user:
                access_token = create_access_token(identity=find_user.idx, expires_delta=False)
                return json.dumps({"token": access_token}), 200
            else:
                return json.dumps({"msg": '로그인에 실패하였습니다. id와 password 를 확인해주세요'}, ensure_ascii=False), 401

        except Exception as e:
            return json.dumps({"msg": str(e)}), 500
