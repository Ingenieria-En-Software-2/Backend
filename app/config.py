import os


class DevConfig():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUNDLE_ERRORS = True
    SECRET_KEY = os.getenv('SECRET_KEY')
