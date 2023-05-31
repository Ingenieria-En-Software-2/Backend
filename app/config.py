from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables de entorno del archivo .env


class DevConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUNDLE_ERRORS = True
