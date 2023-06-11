from os import environ


class DevConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUNDLE_ERRORS = True