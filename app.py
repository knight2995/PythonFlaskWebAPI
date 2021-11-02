from flask import Flask
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app, version='0.1', title='API', description='PythonFlaskWebAPI')

# Controller 등록
from api.Controller.testController import TestNS
api.add_namespace(TestNS, '/todos')


@app.route('/')
def hello():
    return 'Init Test'


if __name__ == "__main__":
    app.run('127.0.0.1', port=5000, debug=True)
