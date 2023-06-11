from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()


def create_app(object_name):
    app = Flask(__name__,template_folder='templates')
    app.config.from_object(object_name)

    app.config.update(dict(
        MAIL_DEFAULT_SENDER = "noreply@flask.com",
        MAIL_SERVER = "smtp.gmail.com",
        MAIL_PORT = 465,
        MAIL_USE_TLS = False,
        MAIL_USE_SSL = True,
        MAIL_DEBUG = False,
        MAIL_USERNAME = "pruebasoswer2@gmail.com",
        MAIL_PASSWORD = "xvfyzzeqmqdjmifi"
    ))

    db.init_app(app)
    migrate.init_app(app, db)
    mail = Mail(app)

    from .auth import create_module as auth_create_module
    from .main import create_module as main_create_module
    from .api import create_module as api_create_module
    from .endpoints_documentation import create_documentation

    auth_create_module(app)
    main_create_module(app)
    api_create_module(app)
    create_documentation(app)

    return app
