from flask import Flask, render_template, request
from flask_restx import Api
from flask_cors import CORS

import boto3
from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

import sys

db = SQLAlchemy()
migrate = Migrate()

s3 = None


def create_app():

    global s3

    app = Flask(__name__,
                static_url_path='',
                static_folder='web/static',
                )

    if app.env == 'development':
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.DeployConfig')

    # 시간 관계상 모두 허용
    CORS(app, resources={r"*": {"origins": "*"}})

    # 추가 미들웨어 구성
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)

    s3 = boto3.client(
        's3',  # 사용할 서비스 이름, ec2이면 'ec2', s3이면 's3', dynamodb이면 'dynamodb'
        aws_access_key_id=app.config['AWS_ACCESS_KEY'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])  # 비밀 엑세스 키


    from app.api.model import user
    from app.api.model import album
    from app.api.model import photo

    api = Api(app, version='0.1', title='API', description='PythonFlaskWebAPI')

    # controller 등록
    from app.api.controller.wise_saying_controller import wise_saying_namespace
    from app.api.controller.dicom_viewer_controller import dicom_viewer_namespace
    from app.api.controller.yolo_controller import yolo_namespace

    from app.api.controller.auth_controller import authNS
    from app.api.controller.user_controller import userNS
    from app.api.controller.photo_controller import photoNS
    from app.api.controller.album_controller import albumNS

    api.add_namespace(wise_saying_namespace, '/wise-saying')
    api.add_namespace(dicom_viewer_namespace, "/dicom-viewer")
    api.add_namespace(yolo_namespace, "/detect-yolo")

    api.add_namespace(authNS, '/auth')
    api.add_namespace(userNS, '/users')
    api.add_namespace(photoNS, '/photos')
    api.add_namespace(albumNS, '/albums')

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

    @app.route("/photoAlbum")
    def photo_album_view():
        return render_template('feature4.html', base_url=app.config['BASE_URL'])

    @app.route("/feature4-register-form")
    def feature4_register_view():
        return render_template('feature4-register-form.html', base_url=app.config['BASE_URL'])

    @app.route("/feature4-login-form")
    def feature4_login_view():
        return render_template('feature4-login-form.html', base_url=app.config['BASE_URL'])

    @app.route("/feature4-make-album-form")
    def feature4_make_album_view():
        return render_template('feature4-make-album-form.html', base_url=app.config['BASE_URL'])

    @app.route("/feature4-read-album-form")
    def feature4_read_album_view():
        return render_template('feature4-read-album-form.html', base_url=app.config['BASE_URL'])

    @app.route("/feature4-albums-form")
    def feature4_albums_view():
        return render_template('feature4-albums-form.html', base_url=app.config['BASE_URL'])

    @app.route("/feature4-photos-form")
    def feature4_photos_view():
        idx = request.args.get('idx')
        return render_template('feature4-photos-form.html', base_url=app.config['BASE_URL'], selected_album_idx=idx)

    return app
