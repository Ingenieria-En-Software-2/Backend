from ...repositories.CrudRepository import CrudRepository
from ...api.user_transactions.schemas import (
    Create_User_Transaction_Schema,
    Update_User_Transaction_Schema,
)
from ...api.user_transactions.models import Currency, UserTransaction
from ...api.user_account.models import UserAccount,AccountType
from sqlalchemy.sql import functions
from sqlalchemy.orm import aliased
from sqlalchemy import or_, func, extract, and_
import datetime
from datetime import datetime, timedelta



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
    def get_transactions_by_day(self,day,role,user_id,account_type):
        """
        Gets transactions by day given the role of the user, his id and the account type that has done the transaction.
        :param day: Today's date that will be compared.
        :param role: Role of the user.
        :param user_id : ID of the user
        :param account_type : Type of account for getting transactions of only one type.
        :return: A list of all the transactions by day, done by the user of if it is an admin, all the daily transactions.
        """
        if role == 1 and account_type == 0: #admin
            return (self.db.session.query(UserTransaction)
                        .filter(UserTransaction.transaction_date == day)
                        .all())
        if role == 1 and account_type != 0:
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id))
                        .filter(UserTransaction.transaction_date == day, AccountType.id==account_type).all())
        if role == 2: #user
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id))
                        .filter(UserTransaction.transaction_date == day, UserTransaction.user_id == user_id,
                            AccountType.id==account_type).all())

    def get_transactions_by_week(self,role,user_id,account_type):
        """
        Gets transactions by week given the role of the user, his id and the account type that has done the transaction.
        :param role: Role of the user.
        :param user_id : ID of the user
        :param account_type : Type of account for getting transactions of only one type.
        :return: A list of all the transactions by week, done by the user of if it is an admin, all the weekly transactions.
        """
        six_days_ago = datetime.today() - timedelta(days = 6)
        if role == 1 and account_type == 0: #ADMIN get all transactions by week 
            return (self.db.session.query(UserTransaction)
                        .filter(UserTransaction.transaction_date >= six_days_ago)
                        .all())
        if role == 1 and account_type != 0: #get all transactions by week done by a certain account type
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id))
                        .filter(UserTransaction.transaction_date >= six_days_ago, AccountType.id==account_type).all())
        if role == 2: #user get all transactions by week done by the user by a certain account type
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id))
                        .filter(UserTransaction.transaction_date >= six_days_ago, UserTransaction.user_id == user_id,
                            AccountType.id==account_type).all())

    def get_transactions_by_month(self, month_number, role,user_id,account_type):
        """
        Gets transactions by month given the role of the user, his id and the account type that has done the transaction.
        :param month_number: Number of the month to look for transactions done in that month.
        :param role: Role of the user.
        :param user_id : ID of the user
        :param account_type : Type of account for getting transactions of only one type.
        :return: A list of all the transactions by month, done by the user of if it is an admin, all the month's transactions.
        """
        if role == 1 and account_type == 0:
            return (self.db.session.query(UserTransaction)
                        .filter(extract('month', UserTransaction.transaction_date) == month_number)
                        .all())
        if role == 1 and account_type != 0:
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id))
                        .filter(extract('month', UserTransaction.transaction_date) == month_number, AccountType.id==account_type).all())
        if role == 2:
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id))
                        .filter(extract('month', UserTransaction.transaction_date) == month_number, UserTransaction.user_id == user_id,
                            AccountType.id==account_type).all())
    def get_months(self,number):
        """
        Gets a list of month numbers given a quarter of the year.
        :param number: Number of the quarter.
        :return: A list of all the months included in a specific quarter.
        """
        if number == 1:
            return [1,2,3]
        elif number == 2:
            return [4,5,6]
        elif number == 3:
            return [7,8,9]
        else:
            return [10,11,12]

    def get_transactions_by_quarter(self, quarter, role,user_id,account_type):
        """
        Gets transactions by quarter given the role of the user, his id and the account type that has done the transaction.
        :param quarter: Number of the quarter that is needed.
        :param role: Role of the user.
        :param user_id : ID of the user
        :param account_type : Type of account for getting transactions of only one type.
        :return: A list of all the transactions by quarter, done by the user of if it is an admin, all the transactions done in the
        wanted quarter.
        """
        MONTHS = self.get_months(quarter)
        if role == 1 and account_type==0:
            return (self.db.session.query(UserTransaction)
                        .filter(extract('month', UserTransaction.transaction_date).in_(MONTHS))
                        .all())
        if role == 1 and account_type != 0:
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id))
                        .filter(extract('month', UserTransaction.transaction_date).in_(MONTHS), AccountType.id==account_type).all())
        if role == 2:
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id))
                        .filter(extract('month', UserTransaction.transaction_date).in_(MONTHS), UserTransaction.user_id == user_id,
                            AccountType.id==account_type).all())

    def get_transactions_by_year(self, year, role,user_id,account_type):
        """
        Gets transactions by year given the role of the user, his id and the account type that has done the transaction.
        :param year: Year that will be compared.
        :param role: Role of the user.
        :param user_id : ID of the user
        :param account_type : Type of account for getting transactions of only one type.
        :return: A list of all the transactions by year, done by the user of if it is an admin, all the yearly transactions.
        """
        if role == 1 and account_type==0:
            return (self.db.session.query(UserTransaction)
                        .filter(extract('year', UserTransaction.transaction_date) == year)
                        .all())
        if role == 1 and account_type != 0:
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id))
                        .filter(extract('year', UserTransaction.transaction_date) == year, AccountType.id==account_type).all())
        if role == 2:
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id))
                        .filter(extract('year', UserTransaction.transaction_date) == year, UserTransaction.user_id == user_id,
                            AccountType.id==account_type).all())

    def get_transactions_by_date(self, date, role,user_id,account_type):
        """
        Gets transactions by date given the role of the user, his id and the account type that has done the transaction.
        :param date: Formatted date that will be compared.
        :param role: Role of the user.
        :param user_id : ID of the user
        :param account_type : Type of account for getting transactions of only one type.
        :return: A list of all the transactions by date, done by the user of if it is an admin, all the transactions done in a specific
        date.
        """
        if role == 1 and account_type == 0:
            return (self.db.session.query(UserTransaction)
                        .filter(UserTransaction.transaction_date == date)
                        .all())
        if role == 1 and account_type != 0:
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id))
                        .filter(UserTransaction.transaction_date == date, AccountType.id==account_type).all())
        if role == 2:
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id))
                        .filter(UserTransaction.transaction_date == date, UserTransaction.user_id == user_id,
                            AccountType.id==account_type).all())

    def get_transactions_by_period(self,start,end,role,user_id,account_type):
        """
        Gets transactions by period given the role of the user, his id and the account type that has done the transaction.
        :param start: Start date.
        :param end: End date.
        :param role: Role of the user.
        :param user_id : ID of the user
        :param account_type : Type of account for getting transactions of only one type.
        :return: A list of all the transactions by period, done by the user of if it is an admin, all the transactions done in the
        period [start,end].
        """
        if role == 1 and account_type==0:
            return (self.db.session.query(UserTransaction)
                        .filter(UserTransaction.transaction_date >= start, UserTransaction.transaction_date <= end)
                        .all())
        if role == 1 and account_type != 0:
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id))
                        .filter(UserTransaction.transaction_date >= start, UserTransaction.transaction_date <= end,
                         AccountType.id==account_type).all())
        if role == 2:
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id))
                        .filter(UserTransaction.transaction_date >= start, UserTransaction.transaction_date <= end, 
                            UserTransaction.user_id == user_id, AccountType.id==account_type).all())

    def get_all_transactions(self,role,user_id,account_type):
        """
        Gets all transactions given the role of the user, his id and the account type that has done the transaction.
        :param role: Role of the user.
        :param user_id : ID of the user
        :param account_type : Type of account for getting transactions of only one type.
        :return: A list of all the transactions done by the user of if it is an admin, all the transactions done by any user.
        """
        if role == 1 and account_type==0:
            return (self.db.session.query(UserTransaction).all())
        if role == 1 and account_type != 0:
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id)).all())
        if role == 2:
            return (self.db.session.query(UserTransaction).join(UserAccount, and_(UserTransaction.origin_account == UserAccount.id))
                        .join(AccountType, and_(UserAccount.account_type_id == AccountType.id))
                        .filter(UserTransaction.user_id == user_id, AccountType.id==account_type).all())

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
