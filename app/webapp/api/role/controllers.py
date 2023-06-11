"""
Module containing the definition of the RoleApi class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to roles.
"""

from flask_restful import fields as fs
from webapp.auth.models import db, Role
from webapp.api.generic.CrudApi import CrudApi
from webapp.repositories.CrudRepository import CrudRepository
from .schemas import Role_Schema, Update_Role_Schema, Get_Role_Schema

role_repository = CrudRepository(Role, db, Role_Schema, Update_Role_Schema)


class RoleApi(CrudApi):
    def __init__(self):
        super().__init__(role_repository, Get_Role_Schema)
