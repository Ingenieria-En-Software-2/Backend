from flask_restful import Api
from .user.controllers import UserApi
from .role.controllers import RoleApi
from flask import Blueprint
from .account_holder.controllers import AccountHolderApi
from .user_account.controllers import UserAccountApi
from .user_transactions.controllers import UserTransactionsApi
from .logger.controllers import Log_EventApi


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

    rest_api.add_resource(
        UserAccountApi,
        "/user_account",
        "/user_account/<int:id>",
    )

    rest_api.add_resource(
        UserTransactionsApi,
        "/user_transactions",
        "/user_transactions/<string:g>/<string:inp>/<int:account_type>",
        "/user_transactions/<int:id>",
    )

    rest_api.add_resource(
        Log_EventApi,
        "/log_event",        
        "/log_event/<int:id>",
    )



    app.register_blueprint(rest_api_bp)
