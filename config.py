import os 

#basedir = os.path.abspath(".")
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY="Hard to guess string"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = "Flasky Admin <xx@xx.com>"
    FLASKY_ADMIN = "xx@xx.com"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "xx@xx.com"
    MAIL_PASSWORD = "xx"
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir,"data-dev.sqlite")

class TestingConfig(Config):
    TESTING = True    
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir,"data-test.sqlite")

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir,"data.sqlite")

config = {
    "development":DevelopmentConfig,
    "testing":TestingConfig,
    "productin":ProductionConfig,
    "default":DevelopmentConfig
}