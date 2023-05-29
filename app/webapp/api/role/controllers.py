from flask_restful import fields
from ...auth.models import db, Role
from ..generic.CrudApi import CrudApi
from ...repositories.CrudRepository import CrudRepository
from .parsers import (
    role_post_parser,
    role_put_parser,
    role_get_parser
)

role_fields = {
    'id' : fields.Integer(),
    'description' : fields.String(),
}

role_repository = CrudRepository(Role, db)
class RoleApi(CrudApi):
    def __init__(self):
        super().__init__(role_repository, role_fields, role_post_parser, 
            role_put_parser, role_get_parser)


