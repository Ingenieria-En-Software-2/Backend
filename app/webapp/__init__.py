from flask import Flask, render_template



def create_app(object_name):
    from .auth.controllers import auth_blueprint
    from .main.controllers import main_blueprint

    app = Flask(__name__)
    app.config.from_object(object_name)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app