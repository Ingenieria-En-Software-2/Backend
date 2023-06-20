from webapp.repositories.CrudRepository import CrudRepository
from ...auth.UserRepository import UserRepository
from ...auth.models import User
from .models import UserAccount
from ..user.schemas import Create_User_Schema_No_Password
from flask import abort


class UserAccountRepository(CrudRepository):
    """
    A repository for managing Acc objects.
    """

    def __init__(self):
        # TODO: Implement this method
        pass

    def get_account_holder_by_login(self, login):
        # TODO: Implement this method
        pass

    def get_user(self):
        # TODO: Implement this method
        pass

    def create(self, **kwargs):
        # TODO: Implement this method
        pass

    def update(self, id, **kwargs):
        # TODO: Implement this method
        pass
