"""
Module containing definitions of schemas for account holder management in the API.
"""

import datetime
import phonenumbers
import pycountry
import re
from ...api.user.schemas import Create_User_Schema
from ...api.user_account.models import UserAccount
from ...auth.models import User
from ...api.generic.GetSchema import Generic_Get_Schema
from marshmallow import (
    Schema,
    fields,
    post_load,
    validate,
    validates,
    ValidationError,
    validates_schema,
)

# Definition of the schemas for validation of account holder data


class Create_User_Account_Schema(Schema):
    # Account holder fields
    id = fields.Integer()
    user_id = fields.Integer(required=True)
    account_number = fields.String(
        required=True,
        validate=validate.Length(
            min=20,
            max=20,
            error="El número de cuenta debe tener 20 caracteres",
        ),
    )
    account_type_id = fields.Integer(required=True)

    @validates("user_id")
    def validate_user_id(self, value):
        # validations for user id
        # check if user id exists in the database
        if not User.query.get(value):
            raise ValidationError("El usuario no existe")

    @validates("account_number")
    def validate_account_number(self, value):
        # validations for account number
        # check if account number is 20 characters long
        # the first 4 characters must be 0150
        # the next 5 characters must be 30000
        # the remaining 11 characters must be numbers
        if not re.match(r"^\d{20}$", value):
            raise ValidationError(
                "El número de cuenta debe tener 20 caracteres")
        if value[0:4] != "0150":
            raise ValidationError("El número de cuenta debe comenzar con 0150")
        if value[4:9] != "30000":
            raise ValidationError(
                "El número de cuenta debe comenzar con 015030000")
        if not value[9:].isdigit():
            raise ValidationError(
                "Los últimos 11 caracteres deben ser números")

    @validates("account_type_id")
    def validate_account_type_id(self, value):
        # validations for account type id
        # check if account type id is 1 or 2
        if value not in [1, 2]:
            raise ValidationError(
                "El tipo de cuenta debe ser 1 (corriente) o 2 (ahorro)")
        # check person type of user id and check the number of accounts
        # natural person can only have one account of each type
        # legal person can only have two savings accounts and six current accounts




class Update_User_Account_Schema(Create_User_Account_Schema):
    # Account holder fields
    id = fields.Integer()
    user_id = fields.Integer(required=True)
    account_number = fields.String(
        required=True,
        validate=validate.Length(
            min=20,
            max=20,
            error="El número de cuenta debe tener 20 caracteres",
        ),
    )
    account_type_id = fields.Integer()
    class Meta:
        exclude = ('id',)

class Get_User_Account_Schema(Generic_Get_Schema):
    # Account holder fields
    user_id = fields.Integer()
    account_number = fields.String()
    account_type_id = fields.Integer()
    user = fields.Nested(Create_User_Schema)

    sort_by = fields.String(
        load_default="user_id",
        validate=validate.OneOf(
            ["id",
             "user_id",
             "account_number",
             "account_type_id"],
            error="El campo sort_by solo puede tomar los valores id, user_id, account_number o account_type_id",
        )
    )
