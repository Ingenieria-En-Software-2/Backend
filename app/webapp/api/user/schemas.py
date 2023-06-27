"""
Module containing definitions of schemas for user management in the API.

Theree schemas are defined: Create_User_Schema, Update_User_Schema and Get_Role_Schema,
each one with its respective arguments and validation rules.
"""

from marshmallow import Schema, fields, validate, validates, ValidationError
from ..generic.GetSchema import Generic_Get_Schema
import re

# Definition of the schemas for validation of user data


class Create_User_Schema(Schema):
    id = fields.Integer()
    login = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=6,
                max=50,
                error="El correo electrónico debe tener entre 6 y 50 caracteres",
            ),
            validate.Email(error="Correo electrónico no válido"),
        ],
    )
    password = fields.String(
        required=True,
        validate=validate.Length(
            min=6,
            max=20,
            error="La contraseña debe tener entre 6 y 20 caracteres",
        ),
    )
    name = fields.String(
        required=True,
        validate=validate.Length(
            min=2,
            max=20,
            error="El nombre debe tener entre 2 y 20 caracteres",
        ),
    )
    lastname = fields.String(
        required=True,
        validate=validate.Length(
            min=2,
            max=20,
            error="El apellido debe tener entre 2 y 20 caracteres",
        ),
    )
    person_type = fields.String(
        required=True,
        validate=validate.Length(
            min=5,
            max=20,
            error="El tipo de persona debe tener entre 4 y 20 caracteres",
        ),
    )

    user_type = fields.String(
        required=True,
        validate=validate.Length(
            min=4,
            max=20,
            error="El tipo de usuario debe tener entre 4 y 20 caracteres",
        ),
    )
    role_id = fields.Integer(required=True)
    verified = fields.String(required=False)

    @validates("name")
    def validate_name(self, value):
        """
        Validates that a user's name contains only letters and spaces. Throws a
        ValidationError exception in case the name does not comply with the
        pattern.
        """
        regex = r"^[a-zA-Z\s]+$"
        if not re.match(regex, value):
            raise ValidationError(
                "El nombre solo puede contener letras y espacios"
            )

    @validates("lastname")
    def validate_lastname(self, value):
        """
        Validates that a user's last name contains only letters and spaces.
        Throws a ValidationError exception in case the last name does not
        comply with the pattern.
        """
        regex = r"^[a-zA-Z\s]+$"
        if not re.match(regex, value):
            raise ValidationError(
                "El apellido solo puede contener letras y espacios"
            )

    @validates("person_type")
    def validate_person_type(self, value):
        """
        Validates that a user's person type contains only letters and spaces.
        Throws a ValidationError exception in case the person type does not
        comply with the pattern.
        """
        allowed_types = ["natural", "legal"]
        if value not in allowed_types:
            raise ValidationError(
                "El tipo de persona solo puede ser natural o legal"
            )


class Update_User_Schema(Create_User_Schema):
    login = fields.String(
        validate=[
            validate.Email(error="Correo electrónico no válido"),
            validate.Length(min=6, max=50),
        ],
    )
    password = fields.String(
        validate=validate.Length(
            min=6,
            max=20,
            error="La contraseña debe tener entre 6 y 20 caracteres",
        ),
    )
    name = fields.String(
        validate=validate.Length(
            min=2,
            max=20,
            error="El nombre debe tener entre 2 y 20 caracteres",
        )
    )
    lastname = fields.String(
        validate=validate.Length(
            min=2,
            max=20,
            error="El apellido debe tener entre 2 y 20 caracteres",
        ),
    )
    user_type = fields.String(
        validate=validate.Length(
            min=4,
            max=20,
            error="El tipo de usuario debe tener entre 4 y 20 caracteres",
        ),
    )
    role_id = fields.Integer()

    class Meta:
        exclude = ("id",)


class Get_User_Schema(Generic_Get_Schema):
    login = fields.String()
    name = fields.String()
    lastname = fields.String()
    user_type = fields.String()
    role_id = fields.Integer()
    verified = fields.Boolean()
    sort_by = fields.Str(
        load_default=None,
        validate=validate.OneOf(
            ["id", "login", "name", "lastname", "user_type", "role_id", "verified"]
        ),
    )


class Create_User_Schema_No_Password(Create_User_Schema):
    password = fields.String(required=False, allow_none=True)
