"""
Schemas for validation of mobile payment configuration data
"""

import datetime
import phonenumbers
import pycountry
import re
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

# Creation schema for mobile payment configuration
class POST_Mobile_Payment_Schema(Schema):
    
    id = fields.Integer()
    user_id = fields.Integer(required=True)
    
    email = fields.String(
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
    account_id = fields.Integer(required=True)
    max_amount = fields.Float(required=True)
    document = fields.String(required=True)
    receiver_name = fields.String(required=True)
    


    @validates("document")
    def validate_document(self, value):
        """
        Validate a person's ID card

        The format of a valid ID card is:
         - Begins with V, E, J, G, C, uppercase or lowercase.
         - Followed by a dash and 7 or 8 digits.
         - May contain spaces or dots as separators.
         - The first digit of the ID card must be different from zero.
        """
        # Removes spaces and dots from the number
        table = str.maketrans("", "", ". ")
        id_number = value.translate(table)

        # Transform to uppercase
        id_number = id_number.upper()

        # Regular expression for validating id numbers
        regex = r"[V|E|J|G|C]-\d{7,8}"
        if not re.fullmatch(regex, id_number):
            raise ValidationError(
                "El número de documento ingresado es inválido, debe tener el "
                + "formato <Tipo>-<número> Posibles valores para tipo: V,J,G,E,C "
                + "y número debe tener entre 7 y 8 dígitos"
            )

    @validates("receiver_name")
    def validate_receiver_name(self, value):
        """
        Validates that a receiver name contains only letters and spaces. Throws a
        ValidationError exception in case the name does not comply with the
        pattern.
        """
        regex = r"^[a-zA-Z\s]+$"
        if not re.match(regex, value):
            raise ValidationError("El nombre del destinatario solo puede contener letras y espacios")
        
    @validates("phone_number")
    def validate_receiver_name(self, value):
        """
        Validates that a receiver name contains only letters and spaces. Throws a
        ValidationError exception in case the name does not comply with the
        pattern.
        """
        regex = r"^+\d{7}$"
        if not re.match(regex, value):
            raise ValidationError("El numero de telefono no tiene el formato correcto")

    @validates("max_amount")
    def validate_max_amount(self, value):
        """
        Validates that the max amount is greater than 0
        """
        if value <= 0:
            raise ValidationError("El monto máximo debe ser mayor a 0")


class GET_Mobile_Payment_Schema(Generic_Get_Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    email = fields.String()
    account_id = fields.Integer()
    max_amount = fields.Float()
    document = fields.String()
    receiver_name = fields.String()
    
    sort_by = fields.Str(
        load_default=None,
        validate=validate.OneOf(
            [
                "id",
                "user_id",
                "email",
                "account_id",
                "max_amount",
                "document",
                "receiver_name",
            ]
        ),
    )
