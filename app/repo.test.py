from app import app
from webapp import db
from webapp.api.user_account.UserAccountRepository import UserAccountRepository
from webapp.api.user_account.models import AccountType
from webapp.auth.models import User, Role
from webapp.api.account_holder.models import AccountHolder

import sys
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


def get_user_by_id(id):
    return User.query.get(id)


def get_role_by_id(id):
    return Role.query.get(id)


def populate_db():
    # add roles
    add_role("admin")
    add_role("user")
    # add users
    add_user("admin", "admin", "admin", "admin", "natural", "admin", 1, True)  # admin_role.id)
    add_user("user", "user", "user", "user", "legal", "user", 2,True)  # user_role.id)
    # add account types
    add_accounts_types()
   


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        # create the database and the db table
        db.create_all()
        populate_db()
        db.session.commit()
   
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

        repo.create(**{
            'user_id': 2,
            'account_number' : '01503000000000000000',
            'account_type_id' : 2
        })
       
        repo.delete(1)
        
        # commit the changes
        db.session.commit()

       