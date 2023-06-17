"""
Module containing the definition of the UserAccountApi class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to account holders.
"""

from flask import abort
from flask_restful import fields
from webapp.auth.models import db
from app.webapp.api.user_account.UserAccountRepository import UserAccountRepository
from webapp.api.generic.CrudApi import CrudApi
from .schemas import (
    Create_User_Account_Schema, Update_User_Account_Schema,
    Get_User_Account_Schema
)

# Instance of the account holder repository
user_account_repository = UserAccountRepository(
    db, Create_User_Account_Schema, Update_User_Account_Schema
)


class UserAccountApi(CrudApi):
    # Call to the base class constructor CrudApi
    def __init__(self):
        super().__init__(
            user_account_repository,  # Repositorio de usuarios
            Get_User_Account_Schema,  # Esquema Get
        )
