from ...repositories.CrudRepository import CrudRepository
from ...api.user_transactions.schemas import (
    Create_User_Transaction_Schema,
    Update_User_Transaction_Schema,
)
from ...api.user_transactions.models import Currency, UserTransaction
from ...api.user_account.models import UserAccount
from sqlalchemy.sql import functions
from sqlalchemy.orm import aliased
from sqlalchemy import or_


class UserTransactionsRepository(CrudRepository):
    """
    A repository for managing Acc objects.
    """

    def __init__(
        self,
        db,
        create_schema=Create_User_Transaction_Schema,
        update_schema=Update_User_Transaction_Schema,
    ):
        super().__init__(UserTransaction, db, create_schema, update_schema)

    def get_account_balance(self, id):
        "Receive the account id and return its balance"

        income = (
            self.db.session.query(functions.sum(self.model.amount))
            .filter_by(destination_account=id)
            .filter_by(transaction_status_id=2)
            .scalar()
        )

        if not income:
            income = 0

        # Transaction between same account owner
        ua = aliased(UserAccount)
        ua2 = aliased(UserAccount)
        outcome_to_same_owner = (
            self.db.session.query(functions.sum(self.model.amount))
            .join(ua, UserTransaction.origin_account == ua.id)
            .join(ua2, UserTransaction.destination_account == ua2.id)
            .filter(
                UserTransaction.origin_account == id,
                or_(
                    UserTransaction.transaction_status_id == 1,
                    UserTransaction.transaction_status_id == 2,
                ),
                ua.user_id == ua2.user_id,
            )
            .scalar()
        )

        # Transactions between diferent account owners have a 5% tax
        outcome_to_diferent_owner = (
            self.db.session.query(functions.sum(self.model.amount) * 1.02)
            .join(ua, UserTransaction.origin_account == ua.id)
            .join(ua2, UserTransaction.destination_account == ua2.id)
            .filter(
                UserTransaction.origin_account == id,
                or_(
                    UserTransaction.transaction_status_id == 1,
                    UserTransaction.transaction_status_id == 2,
                ),
                ua.user_id != ua2.user_id,
            )
            .scalar()
        )

        if not outcome_to_same_owner:
            outcome_to_same_owner = 0
        if not outcome_to_diferent_owner:
            outcome_to_diferent_owner = 0
        outcome = outcome_to_same_owner + outcome_to_diferent_owner

        return income - outcome

    def update_transaction_status_to_finished(self, id):
        self.update(id, transaction_status_id=2)

    def update_transaction_status_to_canceled(self, id):
        self.update(id, transaction_status_id=3)

    def get_transactions_by_user_id(self, user_id):
        """
        Gets transactions by user_id.
        :param user_id: Id of the user that has done the transaction.
        :return: A list of all the transactions made my the user regardless of the account.
        """
        return (
            self.db.session.query(UserTransaction)
            .filter(UserTransaction.user_id == user_id)
            .all()
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

    def get_currency_by_currency_name(self, currency_name):
        """
        Gets a currency object by the currency name.
        :param currency_name: Name that identifies the currency.
        :return: Currency that is associated with the given name.
        """
        return (
            self.db.session.query(Currency)
            .filter(Currency.name == currency_name)
            .first()
        )
