class Config(object):
    None


class DevelopmentConfig(Config):
    DEBUG = True
    BASE_URL = 'http://127.0.0.1:5000'
    PORT = 5000


class DeployConfig(Config):
    DEBUG = False
    BASE_URL = 'http://knight2995.site'
    PORT = 80
