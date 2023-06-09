"""
Module containing the definition of the UserApi class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to users.
"""

from flask_restful import fields as fs
from webapp.auth.models import db
from webapp.auth.UserRepository import UserRepository
from webapp.api.generic.CrudApi import CrudApi
from .schemas import Create_User_Schema, Update_User_Schema, Get_User_Schema


# Instance of the user repository
user_repository = UserRepository(db, Create_User_Schema, Update_User_Schema)


class UserApi(CrudApi):
    # Call to the base class constructor CrudApi
    def __init__(self):
        super().__init__(
            user_repository,  # Repositorio de usuarios
            Get_User_Schema,  # Esquema Get para roles
        )
