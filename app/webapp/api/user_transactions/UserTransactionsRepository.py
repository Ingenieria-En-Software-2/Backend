from webapp.repositories.CrudRepository import CrudRepository
from webapp.api.user_transactions.schemas import (
    Create_User_Transaction_Schema, 
    Update_User_Transaction_Schema)
from webapp.api.user_transactions.models import UserTransaction


class UserTransactionsRepository(CrudRepository):
    """
    A repository for managing Acc objects.
    """

    def __init__(
        self, 
        db, 
        create_schema=Create_User_Transaction_Schema, 
        update_schema=Update_User_Transaction_Schema):
        super().__init__(UserTransaction, db, create_schema, update_schema)

