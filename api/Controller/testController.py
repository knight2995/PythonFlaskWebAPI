from flask_restx import Resource, Namespace

TestNS = Namespace(
    name="Todos",
    description="Todo 리스트를 작성하기 위해 사용하는 API.",
)


@TestNS.route('/<string:text>')
@TestNS.response(200, 'Found')
@TestNS.response(404, 'Not found')
@TestNS.response(500, 'Internal Error')
@TestNS.param('text', 'String value')
class TestController(Resource):
    @TestNS.doc('get')
    def get(self, text):
        return {"text": "hello,world"}

    @TestNS.doc('delete')
    def delete(self, id):
        return '', 204

    @TestNS.doc('put')
    def put(self, id):
        return ""