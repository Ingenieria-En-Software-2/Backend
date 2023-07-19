"""
Module containing the definition of the RoleApi class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to roles.
"""

from flask_restful import fields as fs
from ...auth.models import db, Wallet
from ...api.generic.CrudApi import CrudApi
from ...repositories.CrudRepository import CrudRepository
from .schemas import Wallet_Schema, Update_Wallet_Schema, Get_Wallet_Schema

wallet_repository = CrudRepository(Wallet, db, Wallet_Schema, Update_Wallet_Schema)


class WalletApi(CrudApi):
    def __init__(self):
        super().__init__(wallet_repository, Get_Wallet_Schema)

    def get(self):
        """Get all user account.

        :return: All user accounts
        """
        wallets = db.session.query(Wallet).all()
        list_wallets = list(map(lambda a : {"id" : a.id, "description" : a.description}, wallets))
        return {"wallets" : list_wallets},200
