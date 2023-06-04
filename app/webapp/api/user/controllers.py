
"""
Módulo que contiene la definición de la clase UserApi, la cual hereda de la clase
CrudApi, y se encarga de manejar las peticiones HTTP relacionadas con los usuarios.
"""
from flask_restful import fields as fs
from webapp.auth.models import db
from webapp.auth.UserRepository import UserRepository
from ..generic.CrudApi import CrudApi
from marshmallow import Schema, fields, validate
from .parsers import (
    user_get_parser,
    user_post_parser,
    user_put_parser,
)


class Create_User_Schema(Schema):
    pass

class Update_User_Schema(Schema):
    pass


# Definición de los campos de un usuario para la serialización
user_fields = {
    "id": fs.Integer(),
    "login": fs.String(),
    "password": fs.String(),
    "name": fs.String(),
    "lastname": fs.String(),
    "user_type": fs.String(),
    "role_id": fs.Integer(),
}


# Instancia del repositorio de usuarios
user_repository = UserRepository(db, Create_User_Schema, Update_User_Schema)
class UserApi(CrudApi):
    # Llamada al constructor de la clase base CrudApi
    def __init__(self):
        super().__init__(
            user_repository,  # Repositorio de usuarios
            user_fields,      # Campos de un usuario
            user_post_parser, # Parser para la creación de un usuario
            user_put_parser,  # Parser para la actualización de un usuario
            user_get_parser,  # Parser para la obtención de usuarios
        )
