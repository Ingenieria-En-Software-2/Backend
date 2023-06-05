"""
Módulo que contiene la definición de la clase UserApi, la cual hereda de la clase
CrudApi, y se encarga de manejar las peticiones HTTP relacionadas con los usuarios.
"""

from flask_restful import fields as fs
from webapp.auth.models import db
from webapp.auth.UserRepository import UserRepository
from ..generic.CrudApi import CrudApi
from marshmallow import Schema, fields, validate, validates, ValidationError
from ..generic.GetSchema import Generic_Get_Schema

import re


# Definición de los esquemas para la validación de los datos de un usuario


class Create_User_Schema(Schema):
    id = fields.Integer()
    login = fields.String(required=True, validate=validate.Length(min=4, max=20))
    password = fields.String(required=True, validate=validate.Length(min=6, max=20))
    name = fields.String(required=True, validate=validate.Length(min=2, max=20))
    lastname = fields.String(required=True, validate=validate.Length(min=2, max=20))
    user_type = fields.String(required=True, validate=validate.Length(min=4, max=20))
    role_id = fields.Integer(required=True)

    @validates("login")
    def validate_login(self, value):
        """
        Valida que el login de un usuario solo contenga letras, números y guiones bajos.
        Lanza una excepción ValidationError en caso de que el login no cumpla con el patrón.
        """

        regex = r"^(?![0-9])\w+$"
        if not re.match(regex, value):
            raise ValidationError(
                "El nombre de usuario solo puede contener letras, números y guiones bajos"
            )

    @validates("password")
    def validate_password(self, value):
        """
        Valida que la contraseña de un usuario contenga al menos un número, una letra
        mayúscula, una letra minúscula y un caracter especial. Lanza una excepción
        ValidationError en caso de que la contraseña no cumpla con el patrón.
        """
        # Verifica contenga al menos un número
        if not re.match(r".*\d+.*", value):
            raise ValidationError("La contraseña debe contener al menos un número")

        # Verifica contenga al menos una letra minúscula y una mayúscula
        regex = r"(?=.*[A-Z])(?=.*[a-z]).*"
        if not re.match(regex, value):
            raise ValidationError(
                "La contraseña debe contener al menos una letra mayúscula y una minúscula"
            )

        # Verifica contenga al menos un caracter especial
        regex = r".*[!@#$%^&*(),.?\":{}|<>].*"
        if not re.match(regex, value):
            raise ValidationError(
                "La contraseña debe contener al menos un caracter especial"
            )

    @validates("name")
    def validate_name(self, value):
        """
        Valida que el nombre de un usuario solo contenga letras y espacios. Lanza una
        excepción ValidationError en caso de que el nombre no cumpla con el patrón.
        """
        regex = r"^[a-zA-Z\s]+$"
        if not re.match(regex, value):
            raise ValidationError("El nombre solo puede contener letras y espacios")

    @validates("lastname")
    def validate_lastname(self, value):
        """
        Valida que el apellido de un usuario solo contenga letras y espacios. Lanza una
        excepción ValidationError en caso de que el apellido no cumpla con el patrón.
        """
        regex = r"^[a-zA-Z\s]+$"
        if not re.match(regex, value):
            raise ValidationError("El apellido solo puede contener letras y espacios")


class Update_User_Schema(Create_User_Schema):
    id = fields.Integer()
    login = fields.String(validate=validate.Length(min=4, max=20))
    password = fields.String(validate=validate.Length(min=6, max=20))
    name = fields.String(validate=validate.Length(min=2, max=20))
    lastname = fields.String(validate=validate.Length(min=2, max=20))
    user_type = fields.String(validate=validate.Length(min=4, max=20))
    role_id = fields.Integer()



class Get_Role_Schema(Generic_Get_Schema):
    pass


# Instancia del repositorio de usuarios
user_repository = UserRepository(db, Create_User_Schema, Update_User_Schema)


class UserApi(CrudApi):
    # Llamada al constructor de la clase base CrudApi
    def __init__(self):
        super().__init__(
            user_repository,  # Repositorio de usuarios
            Get_Role_Schema,
        )
