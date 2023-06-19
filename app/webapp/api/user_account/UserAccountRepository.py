from webapp.repositories.CrudRepository import CrudRepository
from .models import UserAccount
from .schemas import Create_User_Account_Schema, Update_User_Account_Schema
from marshmallow import ValidationError
from webapp.auth.models import User

class UserAccountRepository(CrudRepository):
    """
    A repository for managing Acc objects.
    """

    def __init__(
        self, 
        db,
        transactions_repository,
        create_schema=Create_User_Account_Schema, 
        update_schema=Update_User_Account_Schema):
        self.transactions_repository = transactions_repository        
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
    
    def create(self, **kwargs):
        self.check_number_of_accounts(kwargs["user_id"], **kwargs)
        return super().create(**kwargs)

    def update(self, id, **kwargs):        
        self.check_number_of_accounts(id, **kwargs)
        return super().update(id, **kwargs)


    def get_account_balance(self, id):
        "Receive the id of an account and return that account with its balance"        
        account = self.get_by_id(id)
        balance = self.transactions_repository.get_account_balance(id)
        return {'account' : account, 'balance' : balance} 

    
    def get_user_accounts_balances(self, id):
        "Receive the id of a user and return all of the users accounts with their balance"
        accounts = self.get_all(user_id=id)
        accounts_balance = [
            self.get_account_balance(acc.id) for acc in accounts
            ]
        return accounts_balance
