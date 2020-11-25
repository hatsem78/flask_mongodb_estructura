import logging
from dotenv import load_dotenv, find_dotenv
import os
from datetime import timedelta


class Config(object):
    
    def __init__(self):
        load_dotenv(find_dotenv('.env'))
        self.DEBUG = False
        self.TESTING = False
        self.PRODUCTION = False
        self.APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        self.AUTHENTICATION_SOURCE = '',
        self.REDIS_HOST = os.getenv('REDIS_HOST', '0.0.0.0')
        self.REDIS_PORT = os.getenv('REDIS_PORT', 6379)
        self.REDIS_DB = os.getenv('REDIS_DB', 0)

        self.ERROR_INCLUDE_MESSAGE = False

        self.SECRET_KEY = os.getenv('SECRET_KEY', 'My-Precious-Key')
        SECRET_KEY = os.getenv('SECRET_KEY', 'My-Precious-Key')
        self.JWT_SECRET_KEY = SECRET_KEY
        self.JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)
        self.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=365)

        self.JWT_SECRET_KEY = SECRET_KEY
        self.JWT_BLACKLIST_ENABLED = True
        self.JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
        # os.getenv("JWT_ACCESS_CSRF_HEADER_NAME")
        self.JWT_ACCESS_CSRF_HEADER_NAME = SECRET_KEY
        self.JWT_COOKIE_CSRF_PROTECT = True
        self.JWT_COOKIE_DOMAIN = os.getenv("JWT_COOKIE_DOMAIN")

        self.LOG_LEVEL = logging.DEBUG
        self.DB_HOST = os.getenv('DB_HOST', 'localhost')
        self.DB_USER = os.getenv('DB_USER', 'admin')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'abc123')
        self.DB_PORT = os.getenv('DB_PORT', 27017)
        self.DB_NAME = os.getenv('DB_NAME', 'compensar')

        AUTHENTICATION_SOURCE = '',
        try:
            # Python 3.x
            from urllib.parse import quote_plus
        except ImportError:
            # Python 2.x
            from urllib import quote_plus
        self.MONGO_URI = "mongodb://%s:%s@%s" % (
            quote_plus(self.DB_USER), quote_plus(self.DB_PASSWORD), self.DB_HOST + ':' + str(self.DB_PORT) + '/' + self.DB_NAME)
        self.MONGODB_SETTINGS = self.mongo_from_uri(self.MONGO_URI)

    @staticmethod
    def mongo_from_uri(uri):
        print(uri)
        conn_settings = {"host": uri}
        return conn_settings


class Development(Config):
    """
        Use "if app.debug" anywhere in your code,
        that code will run in development mode.
    """

    def __init__(self):
        super(Development, self).__init__()
        self.ENVIRONMENT = "Dev"
        self.DEBUG = True
        self.TESTING = False


class Production(Config):
    def __init__(self):
        super(Development, self).__init__()
        self.ENVIRONMENT = "Prod"
        self.DEBUG = False
        self.TESTING = False


class TestingConfig(Config):
    DEBUG = True
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'abc123')
    DB_PORT = os.getenv('DB_PORT', 27017)
    DB_NAME = os.getenv('DB_NAME', 'compensar')
    AUTHENTICATION_SOURCE = '',
    try:
        # Python 3.x
        from urllib.parse import quote_plus
    except ImportError:
        # Python 2.x
        from urllib import quote_plus
        # client = MongoClient('mongodb://admin:abc123@localhost:27017/compensar')
    MONGO_URI = "mongodb://%s:%s@%s" % (
        quote_plus('admin'), quote_plus('compesar2019'), DB_HOST + ':' + str(DB_PORT) + '/' + DB_NAME)

    MAIL_DEFAULT_SENDER = os.getenv(
        'MAIL_USER', "development.service@gmail.com")
    MAIL_USERNAME = os.getenv('MAIL_USER', "development.service@gmail.com")
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', "Password@123")
    MAIL_SERVER = os.getenv('MAIL_SERVER', "smtp.gmail.com")
    MAIL_PORT = os.getenv('MAIL_PORT', "587")
    MAIL_USE_TLS = True


config_by_name = dict(
    dev=Development,
    test=TestingConfig,
    prod=Production
)
