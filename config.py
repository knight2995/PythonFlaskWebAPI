class Config(object):
    None


class DevelopmentConfig(Config):
    DEBUG = True
    BASE_URL = 'http://127.0.0.1:5000'
    PORT = 5000


class DeployConfig(Config):
    DEBUG = False
    BASE_URL = 'http://13.124.151.134'
    PORT = 80
