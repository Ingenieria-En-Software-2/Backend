"""
Module containing the definition of the UserAccountApi class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to account holders.
"""

from flask import abort
from flask_restful import fields
from webapp.auth.models import db
from webapp.api.user_account.UserAccountRepository import UserAccountRepository
from webapp.api.user_transactions.UserTransactionsRepository import UserTransactionsRepository
from webapp.api.generic.CrudApi import CrudApi
from .schemas import Get_User_Account_Schema

# Instance of the account holder repository
transaction_repository = UserTransactionsRepository(db)
user_account_repository = UserAccountRepository(db, transaction_repository)


class UserAccountApi(CrudApi):
    # Call to the base class constructor CrudApi
    def __init__(self):
        super().__init__(
            user_account_repository,  # Repositorio de usuarios
            Get_User_Account_Schema,  # Esquema Get
        )
