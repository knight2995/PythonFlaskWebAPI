from flask import Flask, render_template
from flask_restx import Api
from flask_cors import CORS

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            )

app.config.from_object('config.DevelopmentConfig')

# 시간 관계상 모두 허용
CORS(app)

api = Api(app, version='0.1', title='API', description='PythonFlaskWebAPI')

# Controller 등록
from api.Controller.wise_saying_controller import wise_saying_namespace

api.add_namespace(wise_saying_namespace, '/wise-saying')


# 테스트를 위한 더미 등록
@app.route("/명언제조기")
def 명언제조기():
    return render_template('feature1.html', base_url=app.config['BASE_URL'])


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)
