from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from webapp.api.generic import mail
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()


def create_app(object_name):
    app = Flask(__name__,template_folder='templates')
    app.config.from_object(object_name)

    db.init_app(app)
    migrate.init_app(app, db)
    mail = Mail(app)
    #mail.init_app(app)

    from .auth import create_module as auth_create_module
    from .main import create_module as main_create_module
    from .api import create_module as api_create_module
    from .endpoints_documentation import create_documentation

    auth_create_module(app)
    main_create_module(app)
    api_create_module(app)
    create_documentation(app)

    return app
