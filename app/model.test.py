from app import app
from webapp import db
from webapp.auth.models import User, Role
from webapp.api.account_holder.models import AccountHolder
import sys


def add_user(login, password, name, lastname, user_type, role_id):
    user = User(login, password, name, lastname, user_type, role_id)
    db.session.add(user)
    db.session.commit()
    return user


def add_account_holder(
    login,
    password,
    name,
    lastname,
    user_type,
    role_id,
    identification_document,
    gender,
    civil_status,
    birthdate,
    phone,
    nacionality,
    street,
    sector,
    city,
    country,
    province,
    township,
    address,
    employer_name,
    employer_rif,
    employer_phone,
    employer_city,
    employer_country,
    employer_province,
    employer_township,
    employer_address,
):
    ah = AccountHolder(
        login,
        password,
        name,
        lastname,
        user_type,
        role_id,
        identification_document,
        gender,
        civil_status,
        birthdate,
        phone,
        nacionality,
        street,
        sector,
        city,
        country,
        province,
        township,
        address,
        employer_name,
        employer_rif,
        employer_phone,
        employer_city,
        employer_country,
        employer_province,
        employer_township,
        employer_address,
    )
    db.session.add(ah)
    db.session.commit()
    return ah


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
    add_user("admin", "admin", "admin", "admin", "admin", 1)  # admin_role.id)
    add_user("user", "user", "user", "user", "user", 2)  # user_role.id)
    # add Account holder
    add_account_holder(
        "login",
        "password",
        "name",
        "lastname",
        "user_type",
        2,
        "identification_document",
        "gender",
        "civil_status",
        "birthdate",
        "phone",
        "nacionality",
        "street",
        "sector",
        "city",
        "country",
        "province",
        "township",
        "address",
        "employer_name",
        "employer_rif",
        "employer_phone",
        "employer_city",
        "employer_country",
        "employer_province",
        "employer_township",
        "employer_address",
    )


if __name__ == "__main__":
    with app.app_context():
        if len(sys.argv) > 1 and sys.argv[1] == "create":
            db.drop_all()
            # create the database and the db table
            db.create_all()
            # commit the changes
            db.session.commit()

        if len(sys.argv) > 1 and sys.argv[1] == "populate":
            populate_db()
