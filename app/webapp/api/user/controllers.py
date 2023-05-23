from flask_restful import fields
from webapp.auth.models import db
from webapp.auth.UserRepository import UserRepository
from ..generic.CrudApi import CrudApi
from .parsers import (
    user_get_parser,
    user_post_parser,
    user_put_parser,
)

user_fields = {
    'id' : fields.Integer(),
    'login' : fields.String(),
    'password' : fields.String(),
    'name' : fields.String(),
    'lastname' : fields.String(),
    'user_type' : fields.String(),
    'role_id' : fields.Integer(),
}

user_repository = UserRepository(db)

class UserApi(CrudApi):
    def __init__(self):
        super().__init__(user_repository, user_fields, user_post_parser, 
            user_put_parser, user_get_parser)
