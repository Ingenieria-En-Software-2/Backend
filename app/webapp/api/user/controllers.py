"""
Módulo que contiene la definición de la clase UserApi, la cual hereda de la clase
CrudApi, y se encarga de manejar las peticiones HTTP relacionadas con los usuarios.
"""

from flask_restful import fields as fs
from webapp.auth.models import db
from webapp.auth.UserRepository import UserRepository
from ..generic.CrudApi import CrudApi
from .schemas import Create_User_Schema, Update_User_Schema, Get_User_Schema


# Instancia del repositorio de usuarios
user_repository = UserRepository(db, Create_User_Schema, Update_User_Schema)


class UserApi(CrudApi):
    # Llamada al constructor de la clase base CrudApi
    def __init__(self):
        super().__init__(
            user_repository,  # Repositorio de usuarios
            Get_User_Schema, # Esquema Get para roles
        )
