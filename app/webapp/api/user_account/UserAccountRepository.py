from webapp.repositories.CrudRepository import CrudRepository
from .models import UserAccount
from .schemas import Create_User_Account_Schema, Update_User_Account_Schema
from marshmallow import ValidationError
from webapp.auth.models import User
from sqlalchemy import func


class UserAccountRepository(CrudRepository):
    """
    A repository for managing Acc objects.
    """

    def __init__(
        self, 
        db, 
        create_schema=Create_User_Account_Schema, 
        update_schema=Update_User_Account_Schema):
        super().__init__(UserAccount, db, create_schema, update_schema)

    def check_number_of_accounts(self, id, **kwargs):
        # check person type of user id and check the number of accounts
        # natural person can only have one account of each type
        # legal person can only have two savings accounts and six current accounts
        if not kwargs.get('account_type_id'): return

        user = User.query.get(id)
        if user.person_type == "natural":
        
            if kwargs['account_type_id'] == 1 and UserAccount.query.filter_by(
                    user_id=user.id, account_type_id=1).first():
                raise ValidationError(
                    "El usuario ya tiene una cuenta corriente")
            if kwargs['account_type_id'] == 2 and UserAccount.query.filter_by(
                    user_id=user.id, account_type_id=2).first():
                raise ValidationError(
                    "El usuario ya tiene una cuenta de ahorro")

        if user.person_type == "legal":
            
            if kwargs['account_type_id'] == 1 and UserAccount.query.filter_by(
                    user_id=user.id, account_type_id=1).count() == 6:
                raise ValidationError(
                    "El usuario ya tiene seis cuentas corrientes")
            if kwargs['account_type_id'] == 2 and UserAccount.query.filter_by(
                    user_id=user.id, account_type_id=2).count() == 2:
                raise ValidationError(
                    "El usuario ya tiene dos cuentas de ahorro")
    
    def luhn_number(self, card_number):
        """Luhn number algorithm"""
        card_number = [int(num) for num in card_number]
        checkDigit = card_number.pop(-1)
        card_number.reverse()
        card_number = [num * 2 if idx % 2 == 0
                    else num for idx, num in enumerate(card_number)]
        card_number = [num - 9 if idx % 2 == 0 and num > 9
                    else num for idx, num in enumerate(card_number)]
        card_number.append(checkDigit)
        checkSum = sum(card_number)

        return checkSum % 10

    def get_user_account_by_id(self, id):
        """
        Gets a user account by id.

        :param id: The id of the user account to retrieve.
        :return: The user account with the specified id, or `None` if no user account was
                 found.
        """
        return (
            self.db.session.query(UserAccount).filter(UserAccount.id == id).first()
        )

    def get_user_account_by_account_number(self, account_number):
        """
        Gets a user account by account_number.

        :param account_number: The account_number of the user account to retrieve.
        :return: The user account with the specified account_number, or `None` if no user account was
                 found.
        """
        return (
            self.db.session.query(UserAccount).filter(UserAccount.account_number == account_number).first()
        )
    
    def get_user_accounts(self):
        """
        Ge all user account.

        :return: All user accounts
        """
        return (
            self.db.session.query(UserAccount).all()
        )
    
    def get_user_accounts_by_user_id(self, user_id):
        """
        Gets a user account by user_id.

        :param user_id: The user_id of the user accounts to retrieve.
        :return: The user accounts with the specified user_id.
        """
        return (
            self.db.session.query(UserAccount).filter(UserAccount.user_id == user_id).all()
        )

    def get_one_user_account_by_type(self, user_id, account_type_id):
        """
        Gets an user account by account_type_id.

        :param user_id: The user_id of the user account to retrieve.
        :param account_type_id:  The account_type_id of the user account to retrieve.
        :return: The user accounts with the specified user_id, or `None` if no user account was
                 found.
        """
        return (
            self.db.session.query(UserAccount).filter(UserAccount.user_id == user_id and UserAccount.account_type_id == account_type_id).first()
        )

    def create(self, **kwargs):
        """
        Creates a new User Account in the database.

        :param kwargs: The keyword arguments to use to create the new record.
        :return: The newly created record.
        """
        self.check_number_of_accounts(kwargs["user_id"], **kwargs)
        last_id = self.db.session.query(func.max(UserAccount.id)).first()[0]
        last_id = "0" if last_id is None else str(last_id)
        zeros = ""
        for i in range(10 - len(last_id)):
            zeros += "0"

        account_number = "015030000" + zeros + last_id 
        account_number += str(self.luhn_number(account_number))

        data = kwargs
        data["account_number"] = account_number

        result = self.schema_create().load(kwargs)

        try:
            # Create the instance
            instance = UserAccount(**result)
            self.db.session.add(instance)
            self.db.session.commit()
            return instance

        except Exception as e:
            self.db.session.rollback()
            raise e
        
        # return super().create(**kwargs)

    def update(self, id, **kwargs):        
        self.check_number_of_accounts(id, **kwargs)   
        return super().update(id, **kwargs)

