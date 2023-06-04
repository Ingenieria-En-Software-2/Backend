"""
Módulo que contiene la definición de la clase UserApi, la cual hereda de la clase
CrudApi, y se encarga de manejar las peticiones HTTP relacionadas con los usuarios.
"""

from flask_restful import fields
from webapp.auth.models import db
from webapp.auth.UserRepository import UserRepository
from ..generic.CrudApi import CrudApi
from .parsers import (
    user_get_parser,
    user_post_parser,
    user_put_parser,
)

# Definición de los campos de un usuario para la serialización
user_fields = {
    "id": fields.Integer(),
    "login": fields.String(),
    "password": fields.String(),
    "name": fields.String(),
    "lastname": fields.String(),
    "user_type": fields.String(),
    "role_id": fields.Integer(),
}

# Instancia del repositorio de usuarios
user_repository = UserRepository(db)


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
