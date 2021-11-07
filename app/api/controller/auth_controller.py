import json

from flask_restx import Resource, Namespace, reqparse

from app.api.model.user import User
from app.api.service import auth_service

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

authNS = Namespace(
    name="auth",
    description="로그인 인증(JWT)",
)


@authNS.route("/test")
class Test(Resource):

    @jwt_required()
    @authNS.doc(security='apikey')
    def get(self):

        return get_jwt_identity(), 200


parser = reqparse.RequestParser()
parser.add_argument('id', required=True)
parser.add_argument('password', required=True)


@authNS.route("/login")
@authNS.response(200, 'Success')
@authNS.response(401, 'Login Error')
@authNS.response(500, 'Internal Error')
class Login(Resource):

    @authNS.expect(parser)
    def post(self):

        args = parser.parse_args()

        # User 객체 생성
        user = User(user_id=args['id'], password=args['password'])

        # 넘어온 id, password 로 해당 User 조회
        try:

            find_user = auth_service.check_id_pw(user)

            if find_user:
                access_token = create_access_token(identity=find_user.idx, expires_delta=False)
                return json.dumps({"token": access_token}), 200
            else:
                return '로그인에 실패하였습니다. id와 password 를 확인해주세요', 401

        except Exception as e:
            return str(e), 500


