from flask import Flask
from flask_restx import Api

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            )
api = Api(app, version='0.1', title='API', description='PythonFlaskWebAPI')

# Controller 등록
from api.Controller.testController import TestNS

api.add_namespace(TestNS, '/todos')

from api.Controller.wise_saying_controller import wise_saying_namespace

api.add_namespace(wise_saying_namespace, '/wise-saying')


@app.route('/')
def hello():
    return 'Init Test'


if __name__ == "__main__":
    app.run('127.0.0.1', port=5000, debug=True)
