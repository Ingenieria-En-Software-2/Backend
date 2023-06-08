from webapp.auth.models import db
from webapp.api.account_holder.AccountHolderRepository import AccountHolderRepository
from ..generic.CrudApi import CrudApi
from .schemas import Create_Account_Holder_Schema, Update_Account_Holder_Schema, Get_Account_Holder_Schema

# Instance of the user repository
account_holder_repository = AccountHolderRepository(db, Create_Account_Holder_Schema,
                                                    Update_Account_Holder_Schema)


class AccountHolderAPI(CrudApi):
    # Call to the base class constructor CrudApi
    def __init__(self):
        super().__init__(
            account_holder_repository,  # Repositorio de usuarios
            Get_Account_Holder_Schema,  # Esquema Get para roles
        )