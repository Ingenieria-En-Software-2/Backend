from datetime import timedelta

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)
    app.config["JWT_SECRET_KEY"] = "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTY4NTgzNTIwOCwiaWF0IjoxNjg1ODM1MjA4fQ.RFNvqSgbTY-5Klr5ogBU8axdrxPoYIriJoJpgpabB6w"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt = JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from .auth import create_module as auth_create_module
    from .main import create_module as main_create_module
    from .api import create_module as api_create_module
    from .endpoints_documentation import create_documentation

    auth_create_module(app)
    main_create_module(app)
    api_create_module(app)
    create_documentation(app)

    return app
