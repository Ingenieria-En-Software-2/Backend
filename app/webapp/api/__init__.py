from flask_restful import Api
from .user.controllers import UserApi
from .role.controllers import RoleApi


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

    rest_api.init_app(app)
