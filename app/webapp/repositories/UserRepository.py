from CrudRepository import CrudRepository
# TODO: Import the User model and the db from app

class UserRepository(CrudRepository):
    """
    A repository for managing User objects.
    """
    # TODO: Call the parent constructor with the imported User and db
    def __init__(self, model, db):
    # def __init__(self):
        # super().__init__(User, db)
        super().__init__(model, db)

    def get_user_by_username(self, username):
        """
        Gets a user by username.

        :param username: The username of the user to retrieve.
        :return: The user with the specified username, or `None` if no user was found.
        """
        return self.db.session.query(self.model).filter_by(username=username).first()

    def get_user_by_email(self, email):
        """
        Gets a user by email.

        :param email: The email of the user to retrieve.
        :return: The user with the specified email, or `None` if no user was found.
        """
        return self.db.session.query(self.model).filter_by(email=email).first()

    def get_users_by_role(self, role, page=1, per_page=None, sort_by=None, sort_order='asc'):
        """
        Gets a list of users by role.

        :param role: The role of the users to retrieve.
        :param page: The page number to retrieve, or `1` to retrieve the first one.
        :param per_page: The number of records per page, or `None` to retrieve all records.
        :param sort_by: The name of the attribute to sort by, or `None` to not sort the records.
        :param sort_order: The sort order, 'desc' for descending or ascending by default.
        :return: A list or `QueryPagination` object of users with the specified role, or an empty list if no users were found.
        """
        query = self.db.session.query(self.model).filter_by(role=role)

        if sort_by is not None:
            if sort_order != 'desc':
                query = query.order_by(getattr(self.model, sort_by).asc())
            else:
                query = query.order_by(getattr(self.model, sort_by).desc())

        if per_page is not None:
            # Error out is false to return empty list instead of 404 error when page is out of range
            records = query.paginate(page=page, per_page=per_page, error_out=False)
        else:
            records = query.all()

        return records