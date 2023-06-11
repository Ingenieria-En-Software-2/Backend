from flask_restful import fields
from webapp.auth.models import db, User
from ..generic.CrudApi import CrudApi
from webapp.repositories.CrudRepository import CrudRepository
from .parsers import verify_post_parser, verify_put_parser, verify_get_parser

verify_fields = {
    "id": fields.Integer(),
}

verify_repository = CrudRepository(User, db)


class VerifyApi(CrudApi):
    def __init__(self):
        super().__init__(
            verify_repository,
            verify_fields,
            verify_post_parser,
            verify_put_parser,
            verify_get_parser,
        )
