from webapp.repositories.CrudRepository import CrudRepository
from ...auth.UserRepository import UserRepository
from ...auth.models import User
from .models import AccountHolder
from flask import abort

# TODO: Import the User model and the db from app


class AccountHolderRepository(CrudRepository):
    """
    A repository for managing Acc objects.
    """

    def __init__(self, db):
        super().__init__(AccountHolder, db)

    def get_account_holder_by_login(self, login):
        """
        Gets a account holder by login.

        :param login: The login of the user to retrieve.
        :return: The user with the specified login, or `None` if no user was found or is not accountholder.
        """
        return (
            self.db.session.query(User)
            .join(AccountHolder)
            .filter(User.id == AccountHolder.user_id and login == User.login)
            .first()
        )

    def get_user(self):
        """
        Gets the user associated to account holder

        :return: The user model to the specific account holder.
        :raises: UserErrorinconsistency if no user was found for the specified account holder.
        """
        user = (
            self.db.session.query(User)
            .join(AccountHolder)
            .filter(AccountHolder.user_id == User.id)
            .first()
        )
        if user:
            return user
        else:
            raise ValueError(
                f"User Error Inconsistency for {self.model.id} account holder"
            )

    def create(self, **kwargs):
        """
        Creates a new User And a new AccountHolder in the database.

        :param kwargs: The keyword arguments to use to create the new record.
        :return: The newly created record.
        """
        try:
            user_data = {
                k: kwargs[k]
                for k in (
                    "login",
                    "name",
                    "lastname",
                    "password",
                    "user_type",
                    "role_id",
                )
            }
            user = User(**user_data)
            self.db.session.add(user)
            self.db.session.commit()
            account_holder_data = {
                k: kwargs[k]
                for k in kwargs.keys()
                if k
                not in ("login", "name", "lastname", "password", "user_type", "role_id")
            }
            account_holder_data["user_id"] = user.id
            return super().create(**account_holder_data)

        except Exception as e:
            print(f"An error occurred while creating the user for account holder: {e}")
            self.db.session.rollback()
            return None

    def update(self, id, **kwargs):
        """
        Updates an existing record in the model.

        :param id: The ID of the record to update.
        :param kwargs: The keyword arguments to use to update the record.
        :return: The updated record.
        """

        instance = self.get_by_id(id)
        if instance is None:
            raise ValueError(f"No record found with id {id}")
        user = self.get_user()
        if user is None:
            raise ValueError(f"No associated user for account holder {id}")
        try:
            for key, value in kwargs.items():
                # Check if the attribute is unique in Account Holder
                if hasattr(self.model, key):
                    column = getattr(self.model, key)
                    if column.unique:
                        raise ValueError(f"Cannot update unique attribute '{key}'")
                    setattr(instance, key, value)
                # Check if the attribute is unique in User
                if hasattr(User, key):
                    column = getattr(User, key)
                    if column.unique:
                        raise ValueError(f"Cannot update unique attribute '{key}'")
                    setattr(user, key, value)
            self.db.session.commit()
            return instance
        except Exception as e:
            self.db.session.rollback()
            print(f"An error occurred while updating the record: {e}")

            return None
