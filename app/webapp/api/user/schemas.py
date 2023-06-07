"""
Module containing definitions of schemas for user management in the API.

Theree schemas are defined: Create_User_Schema, Update_User_Schema and Get_Role_Schema,
each one with its respective arguments and validation rules.
"""

from marshmallow import Schema, fields, validate, validates, ValidationError
from webapp.api.generic.GetSchema import Generic_Get_Schema
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
    login = fields.String(validate=validate.Length(min=4, max=20))
    password = fields.String(validate=validate.Length(min=6, max=20))
    name = fields.String(validate=validate.Length(min=2, max=20))
    lastname = fields.String(validate=validate.Length(min=2, max=20))
    user_type = fields.String(validate=validate.Length(min=4, max=20))
    role_id = fields.Integer()

    class Meta:
        exclude = ("id",)


class Get_User_Schema(Generic_Get_Schema):
    login = fields.String()
    name = fields.String()
    lastname = fields.String()
    user_type = fields.String()
    role_id = fields.Integer()
    sort_by = fields.Str(
        load_default=None,
        validate=validate.OneOf(
            ["id", "login", "name", "lastname", "user_type", "role_id"]
        ),
    )
