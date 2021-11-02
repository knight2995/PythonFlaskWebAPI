import werkzeug.datastructures
from flask_restx import Resource, Namespace, reqparse

from api.Service.dicom_viewer_service import convert_dicom_image_to_png


dicom_viewer_namespace = Namespace(
    name="DICOM Web Viewer",
    description="Dicom 을 웹으로 보기 위한 뷰어",
)


@dicom_viewer_namespace.route('/')
@dicom_viewer_namespace.response(200, 'Found')
@dicom_viewer_namespace.response(404, 'Not found')
@dicom_viewer_namespace.response(500, 'Internal Error')
class DicomViewer(Resource):
    @dicom_viewer_namespace.doc('post')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', location='files',
                            type=werkzeug.datastructures.FileStorage, required=True)

        args = parser.parse_args()

        file_object = args['file']
        v = convert_dicom_image_to_png(file_object)

        return v, 200
