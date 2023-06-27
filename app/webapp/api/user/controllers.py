"""
Module containing the definition of the UserApi class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to users.
"""

from flask_restful import fields as fs
from ... import db
from ...auth.UserRepository import UserRepository
from ..generic.CrudApi import CrudApi
from .schemas import Create_User_Schema, Update_User_Schema, Get_User_Schema

user_fields = {
    "id": fs.Integer(),
    "login": fs.String(),
    "password": fs.String(),
    "name": fs.String(),
    "lastname": fs.String(),
    "user_type": fs.String(),
    "role_id": fs.Integer(),
    "verified": fs.Boolean(),
}

# Instance of the user repository
user_repository = UserRepository(db, Create_User_Schema, Update_User_Schema)


class UserApi(CrudApi):
    # Call to the base class constructor CrudApi
    def __init__(self):
        super().__init__(
            user_repository,  # Repositorio de usuarios
            Get_User_Schema,  # Esquema Get para roles
        )
