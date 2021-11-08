import json

import werkzeug.datastructures
from flask_restx import Resource, Namespace, reqparse

from app.api.service.yolo_service import detect_yolo


yolo_namespace = Namespace(
    name="Yolo Detect",
    description="Yolo-v5 테스트 API",
)

parser = reqparse.RequestParser()
parser.add_argument('file', location='files',
                    type=werkzeug.datastructures.FileStorage,
                    help="이미지 파일",
                    required=True)


@yolo_namespace.route('/')
@yolo_namespace.response(200, 'Success')
@yolo_namespace.response(500, 'Internal Error')
class YoloController(Resource):

    @yolo_namespace.doc('post')
    @yolo_namespace.expect(parser)
    def post(self):

        """ API: Yolo-v5 detect API

        이미지 파일을 업로드하고 전송하면 결과를 확인할 수 있습니다.
        시간이 오래 걸릴 수 있습니다.(성능 상 문제)

        """

        args = parser.parse_args()

        file_object = args['file']

        try:
            detected_image = detect_yolo(file_object)
            return json.dumps({"imgData": detected_image}, ensure_ascii=False), 200

        except Exception as e:
            return json.dumps({"msg": str(e)}, ensure_ascii=False), 500


