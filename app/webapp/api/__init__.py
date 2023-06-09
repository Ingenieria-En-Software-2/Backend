from flask_restful import Api
from .user.controllers import UserApi
from .role.controllers import RoleApi
from flask import Blueprint
from .account_holder.controllers import AccountHolderApi

# Parchear el manejador de excepciones de la API
Api.error_router = lambda self, hnd, e: hnd(e)

rest_api_bp = Blueprint("api", __name__, url_prefix="/api")
rest_api = Api(rest_api_bp)


def create_module(app, **kwargs):
    from .error_handlers import error_handlers

    rest_api.add_resource(
        UserApi,
        "/user",
        "/user/<int:id>",
    )

    rest_api.add_resource(
        RoleApi,
        "/role",
        "/role/<int:id>",
    )

    rest_api.add_resource(
        AccountHolderApi,
        "/account_holder",
        "/account_holder/<int:id>",
    )

    app.register_blueprint(rest_api_bp)
