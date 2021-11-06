import werkzeug.datastructures
from flask_restx import Resource, Namespace, reqparse

from app.api.service.yolo_service import detect_yolo


yolo_namespace = Namespace(
    name="Yolo Detect",
    description="Yolo",
)


@yolo_namespace.route('/')
@yolo_namespace.response(200, 'Found')
@yolo_namespace.response(404, 'Not found')
@yolo_namespace.response(500, 'Internal Error')
class DicomViewer(Resource):
    @yolo_namespace.doc('post')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', location='files',
                            type=werkzeug.datastructures.FileStorage, required=True)

        args = parser.parse_args()

        file_object = args['file']
        v = detect_yolo(file_object)

        return v, 200
