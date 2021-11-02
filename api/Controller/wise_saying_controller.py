import werkzeug.datastructures
from flask_restx import Resource, Namespace, reqparse

from api.Service.wise_saying_service import make_wise_saying


wise_saying_namespace = Namespace(
    name="명언짤 제조기",
    description="명언짤 제조를 위한 API.",
)


@wise_saying_namespace.route('/')
@wise_saying_namespace.response(200, 'Found')
@wise_saying_namespace.response(404, 'Not found')
@wise_saying_namespace.response(500, 'Internal Error')
class WiseSaying(Resource):
    @wise_saying_namespace.doc('post')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', location='files',
                            type=werkzeug.datastructures.FileStorage, required=True)
        parser.add_argument('text', required=True)

        args = parser.parse_args()

        file_object = args['file']
        wise_saying = make_wise_saying(file_object, args['text'])

        return wise_saying, 200
