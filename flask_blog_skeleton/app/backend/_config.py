import logging


class Config(object):
    """
    Common configurations
    """
    # BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    CSRF_ENABLED = True
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 3
    LOGGING_LOCATION = 'app/log/app.log'
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_FORMAT = '%(asctime)s >>> LEVEL NAME: %(levelname)s - PATH NAME: %(pathname)s - MODULE: %(funcName)s - MESSAGE: %(message)s .'


class DelevopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True
    # BCRYPT_LOG_ROUNDS = 4


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """
    Testing configuration
    """

    TESTING = True
    DEBUG = True


app_config = {
    "development": DelevopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
