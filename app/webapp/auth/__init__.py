def create_module(app, **kwargs):
    from .controllers import auth_blueprint
    app.register_blueprint(auth_blueprint)