from webapp.repositories.CrudRepository import CrudRepository
from webapp.api.user_transactions.schemas import (
    Create_User_Transaction_Schema, 
    Update_User_Transaction_Schema)
from webapp.api.user_transactions.models import UserTransaction, Currency


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

    def get_transactions_by_user_id(self, user_id):
        """
        Gets transactions by user_id.

        :param user_id: Id of the user that has done the transaction.
        :return: A list of all the transactions made my the user regardless of the account.
        """
        return (
            self.db.session.query(UserTransaction).filter(UserTransaction.user_id == user_id).all()
        )
    def get_currency_by_currency_id(self, currency_id):
        """
        Gets a currency object by the currency id.

        :param currency_id: Id that identifies the currency.
        :return: Currency that is associated with the given id.
        """
        return (
            self.db.session.query(Currency).filter(Currency.id == currency_id).first()
        )

