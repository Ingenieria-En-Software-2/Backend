from flask import abort
from flask_restful import fields
from webapp.auth.models import db
from webapp.api.account_holder.AccountHolderRepository import AccountHolderRepository
from ..generic.CrudApi import CrudApi
from .parsers import (
    account_holder_get_parser,
    account_holder_post_parser,
    account_holder_put_parser,
)

ah_fields = {
    "id": fields.Integer(),
    "login": fields.String(),
    "password": fields.String(),
    "name": fields.String(),
    "lastname": fields.String(),
    "user_type": fields.String(),
    "role_id": fields.Integer(),
}
ah_fields = {
    "id": fields.Integer(),
    "user_id": fields.Integer(),
    "identification_document": fields.String(),
    "gender": fields.String(),
    "civil_status": fields.String(),
    "birthdate": fields.String(),
    "phone": fields.String(),
    "nacionality": fields.String(),
    "street": fields.String(),
    "sector": fields.String(),
    "city": fields.String(),
    "country": fields.String(),
    "province": fields.String(),
    "township": fields.String(),
    "address": fields.String(),
    "employer_name": fields.String(),
    "employer_rif": fields.String(),
    "employer_phone": fields.String(),
    "employer_city": fields.String(),
    "employer_country": fields.String(),
    "employer_province": fields.String(),
    "employer_township": fields.String(),
    "employer_address": fields.String(),
}
repository = AccountHolderRepository(db)


class AccountHolderAPI(CrudApi):
    def __init__(self):
        super().__init__(
            repository,
            ah_fields,
            account_holder_post_parser,
            account_holder_put_parser,
            account_holder_get_parser,
        )
