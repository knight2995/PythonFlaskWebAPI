import json

import werkzeug.datastructures
from flask_restx import Resource, Namespace, reqparse

from app.api.service.wise_saying_service import make_wise_saying

wise_saying_namespace = Namespace(
    name="명언짤 제조기",
    description="명언짤 제조를 위한 API",
)

parser = reqparse.RequestParser()
parser.add_argument('file', location='files', type=werkzeug.datastructures.FileStorage,
                    help='이미지 파일',
                    required=True)
parser.add_argument('text', required=True, help='삽입할 명언(한글 기준)', location='form')


@wise_saying_namespace.route('/')
@wise_saying_namespace.response(200, 'Success')
@wise_saying_namespace.response(500, 'Internal Error')
class WiseSaying(Resource):
    @wise_saying_namespace.doc('post')
    @wise_saying_namespace.expect(parser)
    def post(self):

        """ API: 명언짤제조 API

        이미지 파일을 업로드하고 전송하면 결과를 확인할 수 있습니다.

        """

        args = parser.parse_args()

        file_object = args['file']

        try:
            wise_saying_image = make_wise_saying(file_object, args['text'])
            return json.dumps({"imgData": wise_saying_image}, ensure_ascii=False), 200

        except Exception as e:
            return json.dumps({"msg": str(e)}, ensure_ascii=False), 500
