from webapp.repositories.CrudRepository import CrudRepository
from .models import User, Role

# TODO: Import the User model and the db from app


class UserRepository(CrudRepository):
    """
    A repository for managing User objects.
    """

    def __init__(self, db):
        super().__init__(User, db)

    def get_user_by_login(self, login):
        """
        Gets a user by login.

        :param login: The login of the user to retrieve.
        :return: The user with the specified login, or `None` if no user was found.
        """
        return self.db.session.query(self.model).filter_by(login=login).first()

    def get_users_by_type(self, user_type):
        """
        Gets users by type.

        :param user_type: The type of the users to retrieve.
        :return: The list of users with the specified type.
        """
        return self.db.session.query(self.model).filter_by(user_type=user_type).all()

    def get_users_by_role_id(
        self, role_id, page=1, per_page=None, sort_by=None, sort_order="asc"
    ):
        """
        Gets a list of users by role.

        :param role_id: The id of the role of the users to retrieve.
        :param page: The page number to retrieve, or `1` to retrieve the first one.
        :param per_page: The number of records per page, or `None` to retrieve all records.
        :param sort_by: The name of the attribute to sort by, or `None` to not sort the records.
        :param sort_order: The sort order, 'desc' for descending or ascending by default.
        :return: A list or `QueryPagination` object of users with the specified role, or an empty list if no users were found.
        """
        query = self.db.session.query(self.model).filter_by(role_id=role_id)

        if sort_by is not None:
            if sort_order != "desc":
                query = query.order_by(getattr(self.model, sort_by).asc())
            else:
                query = query.order_by(getattr(self.model, sort_by).desc())

        if per_page is not None:
            # Error out is false to return empty list instead of 404 error when page is out of range
            records = query.paginate(page=page, per_page=per_page, error_out=False)
        else:
            records = query.all()

        return records

    def get_users_by_role_name(
        self, role_name, page=1, per_page=None, sort_by=None, sort_order="asc"
    ):
        """
        Gets a list of users by role name.

        :param role_name: The name of the role of the users to retrieve.
        :param page: The page number to retrieve, or `1` to retrieve the first one.
        :param per_page: The number of records per page, or `None` to retrieve all records.
        :param sort_by: The name of the attribute to sort by, or `None` to not sort the records.
        :param sort_order: The sort order, 'desc' for descending or ascending by default.
        :return: A list or `QueryPagination` object of users with the specified role name, or an empty list if no users were found.
        """
        query = (
            self.db.session.query(self.model).join(Role).filter(Role.name == role_name)
        )

        if sort_by is not None:
            if sort_order != "desc":
                query = query.order_by(getattr(self.model, sort_by).asc())
            else:
                query = query.order_by(getattr(self.model, sort_by).desc())

        if per_page is not None:
            # Error out is false to return empty list instead of 404 error when page is out of range
            records = query.paginate(page=page, per_page=per_page, error_out=False)
        else:
            records = query.all()

        return records

    def get_user_type(self, id):
        """
        Gets the type of a user by id.

        :param id: The id of the user to retrieve the type for.
        :return: The type of the user with the specified id.
        :raises: ValueError if no user was found with the specified id.
        """
        user = self.db.session.query(self.model).filter_by(id=id).first()
        if user:
            return user.user_type
        else:
            raise ValueError(f"No user found with id {id}")

    def get_user_role(self, id):
        """
        Gets the role of a user by id.

        :param id: The id of the user to retrieve the role for.
        :return: The role of the user with the specified id.
        :raises: ValueError if no user was found with the specified id.
        """
        user = self.db.session.query(self.model).filter_by(id=id).first()
        if user:
            return user.role
        else:
            raise ValueError(f"No user found with id {id}")
