"""
Module containing the definition of the AccountHolderApi class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to account holders.
"""

from flask import abort
from flask_restful import fields
from ...auth.models import db
from ...api.account_holder.AccountHolderRepository import AccountHolderRepository
from ...api.generic.CrudApi import CrudApi
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
