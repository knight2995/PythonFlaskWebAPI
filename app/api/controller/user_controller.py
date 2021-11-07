from flask_restx import Resource, Namespace, reqparse
from app.api.model.user import User

from app.api.service.user_service import register_user
from app.api.custom_exception.common_exception import UserDuplicatedException

userNS = Namespace(
    name="User",
    description="User 관리",
)

parser = reqparse.RequestParser()
parser.add_argument('id', required=True)
parser.add_argument('password', required=True)

# 회원가입
@userNS.route("")
@userNS.response(200, 'Success')
@userNS.response(409, 'Conflict')
@userNS.response(500, 'Internal Error')
class Users(Resource):

    # 회원 가입
    @userNS.expect(parser)
    def post(self):

        """ API: 회원가입 API """

        args = parser.parse_args()

        user = User(user_id=args['id'], password=args['password'])

        try:
            register_user(user)

        except UserDuplicatedException as e:
            return str(e), 409

        except Exception as e:
            return '', 500



