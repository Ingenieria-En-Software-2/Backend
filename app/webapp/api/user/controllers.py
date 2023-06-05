"""
Module containing the definition of the UserApi class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to users.
"""

from flask_restful import fields as fs
from webapp.auth.models import db
from webapp.auth.UserRepository import UserRepository
from ..generic.CrudApi import CrudApi
from marshmallow import Schema, fields, validate, validates, ValidationError
from .parsers import (
    user_get_parser,
    user_post_parser,
    user_put_parser,
)
import re


# Definition of the schemas for validation of user data


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
        Validates that a user's login contains only letters, numbers and
        underscores. Throws a ValidationError exception in case the login does
        not comply with the pattern.
        """

        regex = r"^(?![0-9])\w+$"
        if not re.match(regex, value):
            raise ValidationError(
                "The user name can only contain letters, numbers and underscores."
            )

    @validates("name")
    def validate_name(self, value):
        """
        Validates that a user's name contains only letters and spaces. Throws a
        ValidationError exception in case the name does not comply with the
        pattern.
        """
        regex = r"^[a-zA-Z\s]+$"
        if not re.match(regex, value):
            raise ValidationError("The name can contain only letters and spaces")

    @validates("lastname")
    def validate_lastname(self, value):
        """
        Validates that a user's last name contains only letters and spaces.
        Throws a ValidationError exception in case the last name does not 
        comply with the pattern.
        """
        regex = r"^[a-zA-Z\s]+$"
        if not re.match(regex, value):
            raise ValidationError("The last name can only contain letters and spaces")


class Update_User_Schema(Create_User_Schema):
    id = fields.Integer()
    login = fields.String(validate=validate.Length(min=4, max=20))
    password = fields.String(validate=validate.Length(min=6, max=20))
    name = fields.String(validate=validate.Length(min=2, max=20))
    lastname = fields.String(validate=validate.Length(min=2, max=20))
    user_type = fields.String(validate=validate.Length(min=4, max=20))
    role_id = fields.Integer()



# Definition of a user's fields for serialization
user_fields = {
    "id": fs.Integer(),
    "login": fs.String(),
    "password": fs.String(),
    "name": fs.String(),
    "lastname": fs.String(),
    "user_type": fs.String(),
    "role_id": fs.Integer(),
}


# Instance of the user repository
user_repository = UserRepository(db, Create_User_Schema, Update_User_Schema)


class UserApi(CrudApi):
    # Call to the base class constructor CrudApi
    def __init__(self):
        super().__init__(
            user_repository,  # User repository instance
            user_fields,  # User fields for serialization
            user_post_parser,  # Parser for creating a user
            user_put_parser,  # Parser for updating a user
            user_get_parser,  # Parser for getting a user
        )
