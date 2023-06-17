"""
Module containing definitions of schemas for account holder management in the API.
"""

import datetime
import phonenumbers
import pycountry
import re
from webapp.api.user.schemas import Create_User_Schema
from webapp.api.user_account.models import UserAccount
from webapp.auth.models import User
from .models import UserTransaction, Currency, TransactionStatus
from webapp.api.generic.GetSchema import Generic_Get_Schema
from marshmallow import (
    Schema,
    fields,
    post_load,
    validate,
    validates,
    ValidationError,
    validates_schema,
)


class Create_User_Transaction_Schema(Schema):
    id = fields.Integer()
    user_id = fields.Integer(required=True)
    origin_account = fields.Integer()
    destination_account = fields.Integer()
    amount = fields.Float(required=True)
    transaction_type = fields.String(required=True)
    transaction_date = fields.DateTime(required=True)
    transaction_description = fields.String()
    currency_id = fields.Integer()
    transaction_status_id = fields.Integer()

    @validates("user_id")
    def validate_user_id(self, value):
        # validations for user id
        # check if user id exists in the database
        if not User.query.get(value):
            raise ValidationError("El usuario no existe")

    @validates("origin_account")
    def validate_origin_account(self, value):
        # validations for origin account
        # check if origin account exists in the database
        if not UserAccount.query.get(value):
            raise ValidationError("La cuenta de origen no existe")

    @validates("destination_account")
    def validate_destination_account(self, value):
        # validations for destination account
        # check if destination account exists in the database
        if not UserAccount.query.get(value):
            raise ValidationError("La cuenta de destino no existe")

    @validates("amount")
    def validate_amount(self, value):
        # validations for amount
        # check if amount is a number
        if not isinstance(value, float):
            raise ValidationError("El monto debe ser un número")

    @validates("transaction_type")
    def validate_transaction_type(self, value):
        # validations for transaction type
        # check if transaction type is a string
        if not isinstance(value, str):
            raise ValidationError("El tipo de transacción debe ser un string")

    @validates("transaction_date")
    def validate_transaction_date(self, value):
        # validations for transaction date
        # check if transaction date is a date
        if not isinstance(value, datetime.datetime):
            raise ValidationError("La fecha de transacción debe ser una fecha")

    @validates("transaction_description")
    def validate_transaction_description(self, value):
        # validations for transaction description
        # check if transaction description is a string
        if not isinstance(value, str):
            raise ValidationError(
                "La descripción de la transacción debe ser un string")

    @validates("currency_id")
    def validate_currency_id(self, value):
        # validations for currency id
        # check if currency id exists in the database
        if not Currency.query.get(value):
            raise ValidationError("La moneda no existe en la base de datos")

    @validates("transaction_status_id")
    def validate_transaction_status_id(self, value):
        # validations for transaction status id
        # check if transaction status id exists in the database
        if not TransactionStatus.query.get(value):
            raise ValidationError(
                "El estado de la transacción no existe en la base de datos")

    @validates_schema
    def validate_transaction(self, data, **kwargs):
        # validations for transaction
        # check if origin account and destination account are the same
        if data["origin_account"] == data["destination_account"]:
            raise ValidationError(
                "La cuenta de origen y la cuenta de destino no pueden ser la misma")

        # check if transaction date is in the past
        if data["transaction_date"] > datetime.datetime.now():
            raise ValidationError(
                "La fecha de transacción no puede ser en el futuro")


class Update_User_Transaction_Schema(Create_User_Transaction_Schema):
    id = fields.Integer()
    user_id = fields.Integer(required=True)
    origin_account = fields.Integer()
    destination_account = fields.Integer()
    amount = fields.Float(required=True)
    transaction_type = fields.String(required=True)
    transaction_date = fields.DateTime(required=True)
    transaction_description = fields.String()
    currency_id = fields.Integer()
    transaction_status_id = fields.Integer()


class Get_User_Transaction_Schema(Generic_Get_Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    origin_account = fields.Integer()
    destination_account = fields.Integer()
    amount = fields.Float()
    transaction_type = fields.String()
    transaction_date = fields.DateTime()
    transaction_description = fields.String()
    currency_id = fields.Integer()
    transaction_status_id = fields.Integer()

    sort_by = fields.String(
        validate=validate.OneOf(
            ["id", "user_id", "origin_account", "destination_account", "amount", "transaction_type",
                "transaction_date", "transaction_description", "currency_id", "transaction_status_id"],
            error="El campo de ordenamiento debe ser uno de los siguientes: id, user_id, origin_account, destination_account, amount, transaction_type, transaction_date, transaction_description, currency_id, transaction_status_id"
        )
    )
