from flask_restful import Api
from .user.controllers import UserApi
from .role.controllers import RoleApi
from .account_holder.controllers import AccountHolderAPI


rest_api = Api()


def create_module(app, **kwargs):
    rest_api.add_resource(
        UserApi,
        "/api/user",
        "/api/user/<int:id>",
    )

    rest_api.add_resource(
        RoleApi,
        "/api/role",
        "/api/role/<int:id>",
    )
    
    rest_api.add_resource(
        AccountHolderAPI,
        "/api/account_holder",
        "/api/account_holder/<int:id>",
    )

    rest_api.init_app(app)
