from webapp.repositories.CrudRepository import CrudRepository
from ...auth.UserRepository import UserRepository
from ...auth.models import User
from .models import AccountHolder
from ..user.schemas import Create_User_Schema_No_Password
from flask import abort

# TODO: Import the User model and the db from app


class AccountHolderRepository(CrudRepository):
    """
    A repository for managing Acc objects.
    """

    def __init__(self, db, create_schema, update_schema):
        super().__init__(AccountHolder, db, create_schema, update_schema)

    def get_account_holder_by_login(self, login):
        """
        Gets a account holder by login.

        :param login: The login of the user to retrieve.
        :return: The user with the specified login, or `None` if no user was
                 found or is not accountholder.
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
                f"Error de usuario inconsistente para {self.model.id} account holder,"
            )

    def create(self, **kwargs):
        """
        Creates a new User And a new AccountHolder in the database.

        :param kwargs: The keyword arguments to use to create the new record.
        :return: The newly created record.
        """
        result = self.schema_create().load(kwargs)
        user_data = {}
        for i in (
            "login",
            "name",
            "lastname",
            "password",
            "user_type",
            "role_id",
        ):
            if i in kwargs:
                user_data[i] = kwargs[i]

        user_data["password"] = None

        Create_User_Schema_No_Password().load(user_data)
        try:
            # Create the user
            user = User(**user_data)
            self.db.session.add(user)
            self.db.session.commit()

            # Filter the account holder data to remove the user data
            filtered_data = {
                k: result[k]
                for k in result.keys()
                if k
                not in ("login", "name", "lastname", "password", "user_type", "role_id")
            }
            # Add the user_id to the filtered data
            filtered_data["user_id"] = user.id
            # Create the instance
            instance = AccountHolder(**filtered_data)
            self.db.session.add(instance)
            self.db.session.commit()
            return instance

        except Exception as e:
            self.db.session.rollback()
            raise e

    def update(self, id, **kwargs):
        """
        Updates an existing record in the model.

        :param id: The ID of the record to update.
        :param kwargs: The keyword arguments to use to update the record.
        :return: The updated record.
        """

        instance = self.get_by_id(id)
        if instance is None:
            raise ValueError(f"Registro no encontrado para {id}")
        user = self.get_user()
        if user is None:
            raise ValueError(f"No hay usuario asociado con account holder {id}")

        kwargs["id"] = id
        result = self.schema_update().load(kwargs)
        result.pop("id")

        try:
            for key, value in result.items():
                # Check if the attribute is unique in Account Holder
                if hasattr(self.model, key):
                    setattr(instance, key, value)
                # Check if the attribute is unique in User
                if hasattr(User, key):
                    setattr(user, key, value)
            self.db.session.commit()
            return instance
        except Exception as e:
            self.db.session.rollback()
            print(f"A ocurrido un error al actualizar el registro: {e}") #falta

            return None
