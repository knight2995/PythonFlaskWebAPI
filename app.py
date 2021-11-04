from flask import Flask, render_template
from flask_restx import Api
from flask_cors import CORS

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            )

app.config.from_object('config.DevelopmentConfig')

# 시간 관계상 모두 허용
CORS(app, resources={r"*": {"origins": "*"}})

api = Api(app, version='0.1', title='API', description='PythonFlaskWebAPI')

# Controller 등록
from api.Controller.wise_saying_controller import wise_saying_namespace
from api.Controller.dicom_viewer_controller import dicom_viewer_namespace
from api.Controller.yolo_controller import yolo_namespace
api.add_namespace(wise_saying_namespace, '/wise-saying')
api.add_namespace(dicom_viewer_namespace, "/dicom-viewer")
api.add_namespace(yolo_namespace, "/detect-yolo")



# 테스트를 위한 더미 등록
@app.route("/main")
def mainView():
    return render_template('main.html', base_url=app.config['BASE_URL'])


@app.route("/명언제조기")
def 명언제조기():
    return render_template('feature1.html', base_url=app.config['BASE_URL'])

@app.route("/DICOM뷰어")
def DICOM뷰어():
    return render_template('feature2.html', base_url=app.config['BASE_URL'])


@app.route("/Yolo")
def Yolo():
    return render_template('feature3.html', base_url=app.config['BASE_URL'])


if __name__ == "__main__":
    app.run('0.0.0.0', port=app.config['PORT'])
