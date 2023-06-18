"""
Module containing the definition of the UserTransactionsApi class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to account holders.
"""

from flask import abort
from flask_restful import fields
from webapp.auth.models import db
from .UserTransactionsRepository import UserTransactionsRepository
from webapp.api.generic.CrudApi import CrudApi
from .schemas import (
    Create_User_Transaction_Schema,
    Update_User_Transaction_Schema,
    Get_User_Transaction_Schema,
)

# Instance of the account holder repository
user_transactions_repository = UserTransactionsRepository(
    db, Create_User_Transaction_Schema, Update_User_Transaction_Schema
)


class UserTransactionsApi(CrudApi):
    # Call to the base class constructor CrudApi
    def __init__(self):
        super().__init__(
            user_transactions_repository,  # Repositorio de transacciones
            Get_User_Transaction_Schema,  # Esquema Get para roles
        )
