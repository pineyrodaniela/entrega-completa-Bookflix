import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"



class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WHOOSh_BASE = 'whoosh'
    SECRET_KEY = "12345"

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = dbdir
    SECRET_KEY = os.environ["SECRET_KEY"]


class DevelopmentConfig(Config):
    DEBUG = True