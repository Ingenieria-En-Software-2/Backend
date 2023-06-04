from flask_restful import fields as fs
from webapp.auth.models import db
from webapp.auth.UserRepository import UserRepository
from ..generic.CrudApi import CrudApi
from marshmallow import Schema, fields, validate
from .parsers import (
    user_get_parser,
    user_post_parser,
    user_put_parser,
)

class Create_User_Schema(Schema):
    pass

class Update_User_Schema(Schema):
    pass

user_fields = {
    "id": fs.Integer(),
    "login": fs.String(),
    "password": fs.String(),
    "name": fs.String(),
    "lastname": fs.String(),
    "user_type": fs.String(),
    "role_id": fs.Integer(),
}

user_repository = UserRepository(db, Create_User_Schema, Update_User_Schema)


class UserApi(CrudApi):
    def __init__(self):
        super().__init__(
            user_repository,
            user_fields,
            user_post_parser,
            user_put_parser,
            user_get_parser,
        )
