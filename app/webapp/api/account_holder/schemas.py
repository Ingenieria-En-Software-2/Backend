"""
Module containing definitions of schemas for account holder management in the API.
"""

from marshmallow import Schema, fields, validate, validates, ValidationError
from webapp.api.generic.GetSchema import Generic_Get_Schema
import re
import datetime
import phonenumbers
import pycountry

# Definition of the schemas for validation of account holder data


class Create_Account_Holder_Schema(Schema):
    id = fields.Integer()
    user_id = fields.Integer(required=True)
    id_number = fields.String(required=True)
    gender = fields.String(
        required=True,
        validate=validate.OneOf(
            ["M", "F", "O"],
            error="The gender must have be one of the following: M, F, O"
        )
    )
    civil_status = fields.String(
        required=True,
        validate=validate.OneOf(
            ["S", "C", "D", "V"],
            error="The civil status must be one of the following: S, C, D, V"
        )
    )
    birthdate = fields.String(
        required=True,
        Validate=validate.Regexp(
            r"\d{2}-\d{2}-\d{4}",
            error="The birthdate must have the format DD-MM-YYYY"
        )
    )
    phone = fields.String(required=True)
    nacionality = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=30,
                error="The nacionality must have between 3 and 30 characters"
            ),
            validate.Regexp(
                r"^[a-zA-Z]+$",
                error="The nacionality must only contain letters"
            )
        ]
    )
    street = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=50,
                error="The street must have between 3 and 50 characters"
            ),
            validate.Regexp(
                r"[a-zA-Z0-9\s\.\-\/#]",
                error="The street must only contain spaces, letters, numbers and the characters . - / #"
            )
        ]
    )
    sector = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=50,
                error="The sector must have between 3 and 50 characters"
            ),
            validate.Regexp(
                r"[a-zA-Z0-9\s\.\-\/#]",
                error="The sector must only contain spaces, letters, numbers and the characters . - / #"
            )
        ]
    )
    city = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=40,
                error="TThe city must have between 3 and 40 characters"
            ),
            validate.Regexp(
                r"^[a-zA-Z]+$",
                error="The city must only contain letters"
            )
        ]
    )
    country = fields.String(required=True)
    province = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=50,
                error="The province must have between 3 and 50 characters"
            ),
            validate.Regexp(
                r"^[a-zA-Z]+",
                error="The province must only contain letters"
            )
        ]
    )
    township = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=40,
                error="The township must have between 3 and 40 characters"
            ),
            validate.Regexp(
                r"^[a-zA-Z]+",
                error="The township must only contain letters"
            )
        ]
    )
    address = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=50,
                error="The address must have between 3 and 50 characters"
            ),
            validate.Regexp(
                r"[a-zA-Z0-9\s\.\-\/#]",
                error="The address must only contain spaces, letters, numbers and the characters . - / #"
            )
        ]
    )
    employer_name = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=40,
                error="The employer name must have between 3 and 40 characters"
            ),
            validate.Regexp(
                r"^[a-zA-Z\s]+$",
                error="The employer name must only contain spaces and letters"
            )
        ]
    )
    employer_rif = fields.String(
        required=True,
        validate=validate.Regexp(
            r"^[V|E|J|P|G|v|e|j|p|g]-\d{7,8}-\d$",
            error="The employer RIF must have the format V-12345678-9"
        )
    )
    employer_phone = fields.String(required=True)
    employer_city = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=40,
                error="The employer city must have between 3 and 40 characters"
            ),
            validate.Regexp(
                r"^[a-zA-Z\s]+$",
                error="The employer city must only contain spaces and letters"
            )
        ]
    )
    employer_country = fields.String(required=True)
    employer_province = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=50,
                error="The employer province must have between 3 and 50 characters"
            ),
            validate.Regexp(
                r"^[a-zA-Z]+",
                error="The employer province must only contain letters"
            )
        ]
    )
    employer_township = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=40,
                error="The employer township must have between 3 and 40 characters"
            ),
            validate.Regexp(
                r"^[a-zA-Z]+",
                error="The township must only contain letters"
            )
        ]
    )
    employer_address = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=50,
                error="The employer address must have between 3 and 50 characters"
            ),
            validate.Regexp(
                r"[a-zA-Z0-9\s\.\-\/#]",
                error="The employer address entered is invalid, it must have only letters, numbers, spaces, and the following characters: ., -, /, #"
            )
        ]
    )
                

    @validates("id_number")
    def validate_id(self, value):
        """
        Validate a person's ID card
        
        The format of a valid ID card is:
         - Begins with V, E, J, G, C, uppercase or lowercase.
         - Followed by a dash and 7 or 8 digits.
         - May contain spaces or dots as separators.
         - The first digit of the ID card must be different from zero.
            
        Returns the ID card transformed to a standard format:
         - Begins with uppercase.
         - Followed by a dash and 7 or 8 digits.
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
                "The id number entered is invalid, it must have the format V-12345678"
            )


    @validates("birthdate")
    def validate_birthdate(self, value):
        """
        Throws an exception if the birthdate is not valid

        A valid birthdate is:
         - Minimum age is 18 years.
         - Maximum age is 100 years.
        """

        # Convert birthdate a tipo Date using datetime library
        y, m, d = value.split("-")
        y, m, d = int(y), int(m), int(d)
        birthdate_t = datetime.date(y, m, d)
        
        today = datetime.date.today()
        age = (
            today.year
            - birthdate.year
            - ((today.month, today.day) < (birthdate.month, birthdate.day))
        )

        if age < 18:
            raise ClientError("The minimum age to register is 18 years")
        elif age > 100:
            raise ClientError("The maximun age to register is 100 years")
    

    @validates("phone")
    def validate_phone(self, value):
        """
        Throws an exception if the phone number is not valid

        A phone number is valid if it is a valid number in the country entered.
        """
        # Get the country code from the country name
        country = pycountry.countries.search_fuzzy(self.country)[0]
        iso_code = country.alpha_2

        # Validate the phone number using the country code
        phone_number = phonenumbers.parse(value, iso_code)
        is_valid = phonenumbers.is_valid_number(phone_number)

        if not is_valid:
            raise ValidationError("The phone number entered is invalid")


    @validates("country")
    def validate_country(self, value):
        country = pycountry.countries.search_fuzzy(value)[0]
        if country is None:
            raise ValidationError("The country entered is invalid")

        
    @validates("employer_phone")
    def validate_employer_phone(self, value):
        """
        Throws an exception if the phone number is not valid

        A employer phone number is valid if it is a valid number in the country entered.
        """
        # Get the country code from the country name
        country = pycountry.countries.search_fuzzy(self.country)[0]
        iso_code = country.alpha_2

        # Validate the phone number using the country code
        phone_number = phonenumbers.parse(value, iso_code)
        is_valid = phonenumbers.is_valid_number(phone_number)

        if not is_valid:
            raise ValidationError("The employer phone number entered is invalid")


    @validates("employer_country")
    def validate_employer_country(self, value):
        """
        Throws an exception if employer country is not valid
        """
        country = pycountry.countries.search_fuzzy(value)[0]
        if country is None:
            raise ValidationError("The employer country entered is invalid")


class Update_Account_Holder_Schema(Create_Account_Holder_Schema):
    pass


class Get_Account_Holder_Schema(Generic_Get_Schema):
    pass
