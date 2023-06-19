from app import app
from webapp import db
from webapp.api.user_transactions.UserTransactionsRepository import UserTransactionsRepository
from webapp.api.user_account.UserAccountRepository import UserAccountRepository
from webapp.api.user_account.models import AccountType
from webapp.auth.models import User, Role
from webapp.api.account_holder.models import AccountHolder
from webapp.api.user_transactions.models import (
    Currency,
    TransactionStatus,
    UserTransaction
)
import datetime


def add_user(login, password, name, lastname, person_type, user_type, role_id, verified=False):
    user = User(login, password, name, lastname, person_type, user_type, role_id, verified)
    db.session.add(user)
    db.session.commit()
    return user

def add_accounts_types():
    db.session.add(AccountType('Corriente'))
    db.session.add(AccountType('Ahorro'))
    db.session.commit()

def add_users(users):
    db.session.add_all(users)
    db.session.commit()
    return users


def add_role(description):
    role = Role(description)
    db.session.add(role)
    db.session.commit()
    return role


def add_roles(roles):
    db.session.add_all(roles)
    db.session.commit()
    return roles

def create_accounts():
    repo = UserAccountRepository(db)
    repo.create(**{
        'user_id': 1,
        'account_number' : '01503000000000000000',
        'account_type_id' : 1
    })

    repo.create(**{
        'user_id': 1,
        'account_number' : '01503000000000000000',
        'account_type_id' : 2
    })

    repo.create(**{
        'user_id': 2,
        'account_number' : '01503000000000000000',
        'account_type_id' : 2
    })

    repo.delete(3)

def add_currency():
    cs = [
        Currency('dolar', '$', 'USD'),
        Currency('bolivar', 'Bs.S', 'BS.S')
        ]
    db.session.add_all(cs)
    db.session.commit()

def add_transaction_status():
    tss = [
        TransactionStatus('En proceso'),
        TransactionStatus('Finalizada'),
        TransactionStatus('Cancelada')
    ]
    db.session.add_all(tss)
    db.session.commit()

def populate_db():
    # add roles
    add_role("admin")
    add_role("user")
    # add users
    add_user("admin", "admin", "admin", "admin", "natural", "admin", 1, True)  # admin_role.id)
    add_user("user", "user", "user", "user", "legal", "user", 2,True)  # user_role.id)
    # add account types    
    add_accounts_types()
    create_accounts()
    add_currency()
    add_transaction_status()
    

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        # create the database and the db table
        db.create_all()
        populate_db()
        db.session.commit()

        repo = UserTransactionsRepository(db)
        for i in range(1,5):
            repo.create(**{
                'transaction_type' : 'Paypal',
                'transaction_date' : str(datetime.datetime.now()),
                'user_id' : 1,
                'amount' : 500,
                'currency_id' : 1,
                'origin_account': 1,
                'destination_account' : 2,
                'transaction_status_id' : 1,
                'transaction_description' : 'testing'
            })

        repo.update(1, **{'transaction_status_id': 3})

        repo.delete(1)
        repo.delete(3)
        
        # commit the changes
        db.session.commit()

       