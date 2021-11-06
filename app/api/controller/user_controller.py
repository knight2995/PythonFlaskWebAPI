from flask_restx import Resource, Namespace, reqparse
from app.api.model.user import User

from app.api.service.user_service import register_member

userNS = Namespace(
    name="User",
    description="User 관리",
)

# 회원가입
@userNS.route("")
class Users(Resource):

    # 자기 자신 정보 확인
    def get(self):
        return 'Not Implemented', 200

    # 회원 가입
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True)
        parser.add_argument('password', required=True)

        args = parser.parse_args()

        user = User(user_id=args['id'], password=args['password'])
        register_member(user)



