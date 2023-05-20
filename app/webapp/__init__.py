from flask import Flask


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    from .auth import create_module as auth_create_module    
    from .main import create_module as main_create_module
    from .api import create_module as api_create_module

    auth_create_module(app)
    main_create_module(app)
    api_create_module(app)
    

    return app