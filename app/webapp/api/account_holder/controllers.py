"""
Module containing the definition of the AccountHolderApi class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to account holders.
"""

from flask import abort
from flask_restful import fields
from webapp.auth.models import db
from webapp.api.account_holder.AccountHolderRepository import AccountHolderRepository
from webapp.api.generic.CrudApi import CrudApi
from .schemas import (
    Create_Account_Holder_Schema,
    Update_Account_Holder_Schema,
    Get_Account_Holder_Schema,
)

# Instance of the account holder repository
account_holder_repository = AccountHolderRepository(
    db, Create_Account_Holder_Schema, Update_Account_Holder_Schema
)


class AccountHolderApi(CrudApi):
    # Call to the base class constructor CrudApi
    def __init__(self):
        super().__init__(
            account_holder_repository,  # Repositorio de usuarios
            Get_Account_Holder_Schema,  # Esquema Get para roles
        )


# ah_fields = {
#    "id": fields.Integer(),
#    "login": fields.String(),
#    "password": fields.String(),
#    "name": fields.String(),
#    "lastname": fields.String(),
#    "user_type": fields.String(),
#    "role_id": fields.Integer(),
# }
# ah_fields = {
#    "id": fields.Integer(),
#    "user_id": fields.Integer(),
#    "identification_document": fields.String(),
#    "gender": fields.String(),
#    "civil_status": fields.String(),
#    "birthdate": fields.String(),
#    "phone": fields.String(),
#    "nacionality": fields.String(),
#    "street": fields.String(),
#    "sector": fields.String(),
#    "city": fields.String(),
#    "country": fields.String(),
#    "province": fields.String(),
#    "township": fields.String(),
#    "address": fields.String(),
#    "employer_name": fields.String(),
#    "employer_rif": fields.String(),
#    "employer_phone": fields.String(),
#    "employer_city": fields.String(),
#    "employer_country": fields.String(),
#    "employer_province": fields.String(),
#    "employer_township": fields.String(),
#    "employer_address": fields.String(),
# }
