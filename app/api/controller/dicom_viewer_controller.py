import werkzeug.datastructures
from flask_restx import Resource, Namespace, reqparse

from app.api.service.dicom_viewer_service import convert_dicom_image_to_png


dicom_viewer_namespace = Namespace(
    name="DICOM Web Viewer",
    description="Dicom 을 웹으로 보기 위한 뷰어",
)

parser = reqparse.RequestParser()
parser.add_argument('file', location='files',
                    type=werkzeug.datastructures.FileStorage, required=True,
                    help='.dcm 파일(1장짜리)')

parser.add_argument('type', required=True, help='standard or all')


@dicom_viewer_namespace.route('/')
@dicom_viewer_namespace.response(200, 'Found')
@dicom_viewer_namespace.response(500, 'Internal Error')
class DicomViewer(Resource):
    @dicom_viewer_namespace.doc('post')
    @dicom_viewer_namespace.expect(parser)
    def post(self):

        args = parser.parse_args()

        file_object = args['file']
        try:
            result = convert_dicom_image_to_png(file_object, args['type'])
            return result, 200

        except Exception as e:
            return 'Internal Error', 500


