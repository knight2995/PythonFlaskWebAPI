import secret_config


class Config(object):
    SQLALCHEMY_DATABASE_URI = secret_config.db_connection_key
    AWS_ACCESS_KEY = secret_config.aws_access_key_id
    AWS_SECRET_ACCESS_KEY = secret_config.aws_secret_access_key
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = secret_config.jwt_secret_key
    RESTX_MASK_SWAGGER = False


class DevelopmentConfig(Config):
    DEBUG = True
    BASE_URL = 'http://127.0.0.1:5000'
    PORT = 5000


class DeployConfig(Config):
    DEBUG = False
    BASE_URL = 'http://knight2995.site'
    PORT = 80
