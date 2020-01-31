import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = os.environ.get("DEBUG", default=False)
    TESTING = os.environ.get("TESTING", default=False)
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", default=False)

