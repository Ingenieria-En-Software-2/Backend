from flask_restful import fields as fs
from webapp.auth.models import db, Role
from ..generic.CrudApi import CrudApi
from webapp.repositories.CrudRepository import CrudRepository
from .parsers import role_post_parser, role_put_parser, role_get_parser
from marshmallow import Schema, fields, validate


class Create_Role_Schema(Schema):
    description = fields.Str(validate=validate.Length(min=1), required=True)

class Update_Role_Schema(Schema):
    description = fields.Str(validate=validate.Length(min=1))

role_fields = {
    "id": fs.Integer(),
    "description": fs.String(),
}

role_repository = CrudRepository(Role, db, Create_Role_Schema, Update_Role_Schema)


class RoleApi(CrudApi):
    def __init__(self):
        super().__init__(
            role_repository,
            role_fields,
            role_post_parser,
            role_put_parser,
            role_get_parser,
        )
