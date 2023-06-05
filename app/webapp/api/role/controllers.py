from flask_restful import fields as fs
from webapp.auth.models import db, Role
from ..generic.CrudApi import CrudApi
from webapp.repositories.CrudRepository import CrudRepository
from .schemas import Role_Schema, Update_Role_Schema, Get_Role_Schema

role_repository = CrudRepository(Role, db, Role_Schema, Update_Role_Schema)

class RoleApi(CrudApi):
    def __init__(self):
        super().__init__(
            role_repository,
            Get_Role_Schema
        )
