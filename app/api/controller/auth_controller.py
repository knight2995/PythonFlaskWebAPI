import json

from flask_restx import Resource, Namespace, reqparse

from app.api.model.user import User
from app.api.service import auth_service

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

authNS = Namespace(
    name="auth",
    description="회원가입 및 인증",
)


@authNS.route("/test")
class Test(Resource):

    @jwt_required()
    def get(self):

        return get_jwt_identity(), 200


@authNS.route("/login")
class Login(Resource):

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True)
        parser.add_argument('password', required=True)

        args = parser.parse_args()

        user = User(user_id=args['id'], password=args['password'])

        find_user = auth_service.check_id_pw(user)

        if find_user:
            access_token = create_access_token(identity=find_user.idx, expires_delta=False)
            return json.dumps({"token": access_token}), 200
        else:
            return '', 403


