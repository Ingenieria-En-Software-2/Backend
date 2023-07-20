
from ...repositories.CrudRepository import CrudRepository
from ...auth.models import User
from .models import MobilePaymentConfig
from flask import url_for, render_template

class MobilePaymentConfigRepository(CrudRepository):
    """
    A repository for managing User objects.
    """

    def __init__(self, db, create_schema, update_schema):
        super().__init__(MobilePaymentConfig, db, create_schema, update_schema)

    def get_config_by_email(self, email):
        """
        Gets a config by email.

        :param email: The email of the user to retrieve.
        :return: The configuration with the specified email, or `None` if no user was found.
        """
        return self.db.session.query(self.model).filter_by(email=email).first()

    def get_config_by_phone_number(self, phone_number):
        """
        Gets config by phone number.

        :param phone_number: The type of the users to retrieve.
        :return: The list of users with the specified type.
        """
        return self.db.session.query(self.model).filter_by(phone_number=phone_number).all()

    def get_config_by_user_id(
        self, user_id, page=1, per_page=None, sort_by=None, sort_order="asc"
    ):
        """
        Gets a list of config by receiver name

        :param user_id: The id of the user to retrieve.
        :param page: The page number to retrieve, or `1` to retrieve the first one.
        :param per_page: The number of records per page, or `None` to retrieve all records.
        :param sort_by: The name of the attribute to sort by, or `None` to not sort the records.
        :param sort_order: The sort order, 'desc' for descending or ascending by default.
        :return: A list or `QueryPagination` object of users with the specified user id, or an empty list if no users were found.
        """
        query = self.db.session.query(self.model).filter_by(user_id=user_id)

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