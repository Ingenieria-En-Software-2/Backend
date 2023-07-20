
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
        self, user_id
    ):
        """Get config by user id

        Args:
            user_id (int): User id

        Returns:
            MobilePaymentConfig: Mobile payment config
        """
        query = self.db.session.query(self.model).filter_by(user_id=user_id).first()
        return query