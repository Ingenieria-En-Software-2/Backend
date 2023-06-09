"""
Module containing definitions of schemas for account holder management in the API.
"""

from marshmallow import Schema, fields, validate, validates, ValidationError, validates_schema
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
            error="The gender must have be one of the following: M, F, O",
        ),
    )
    civil_status = fields.String(
        required=True,
        validate=validate.OneOf(
            ["S", "C", "D", "V"],
            error="The civil status must be one of the following: S, C, D, V",
        ),
    )
    birthdate = fields.String(
        required=True,
        Validate=validate.Regexp(
            r"\d{2}-\d{2}-\d{4}", error="The birthdate must have the format MM-DD-YYYY"
        ),
    )
    phone = fields.String(required=True)
    nacionality = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=30,
                error="The nacionality must have between 3 and 30 characters",
            ),
            validate.Regexp(
                r"^[a-zA-Z]+$", error="The nacionality must only contain letters"
            ),
        ],
    )
    street = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3, max=50, error="The street must have between 3 and 50 characters"
            ),
            validate.Regexp(
                r"[a-zA-Z0-9\s\.\-\/#]",
                error="The street must only contain spaces, letters, numbers and the characters . - / #",
            ),
        ],
    )
    sector = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3, max=50, error="The sector must have between 3 and 50 characters"
            ),
            validate.Regexp(
                r"[a-zA-Z0-9\s\.\-\/#()]+",
                error="The sector must only contain spaces, letters, numbers and the characters . - / # ( )",
            ),
        ],
    )
    city = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3, max=40, error="TThe city must have between 3 and 40 characters"
            ),
            validate.Regexp(r"^[a-zA-Z\s]+$", error="The city must only contain letters and spaces"),
        ],
    )
    country = fields.String(required=True)
    province = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=50,
                error="The province must have between 3 and 50 characters",
            ),
            validate.Regexp(
                r"^[a-zA-Z\s]+", error="The province must only contain letters and spaces"
            ),
        ],
    )
    township = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=40,
                error="The township must have between 3 and 40 characters",
            ),
            validate.Regexp(
                r"^[a-zA-Z\s]+", error="The township must only contain letters and spaces"
            ),
        ],
    )
    address = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3, max=50, error="The address must have between 3 and 50 characters"
            ),
            validate.Regexp(
                r"[a-zA-Z0-9\s\.\-\/#()]+",
                error="The address must only contain spaces, letters, numbers and the characters . - / # ( )",
            ),
        ],
    )
    employer_name = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=40,
                error="The employer name must have between 3 and 40 characters",
            ),
            validate.Regexp(
                r"^[a-zA-Z\s]+$",
                error="The employer name must only contain spaces and letters",
            ),
        ],
    )
    employer_rif = fields.String(
        required=True,
        validate=validate.Regexp(
            r"^[V|E|J|P|G|v|e|j|p|g]-\d{7,8}-\d$",
            error="The employer RIF must have the format V-12345678-9",
        ),
    )
    employer_phone = fields.String(required=True)
    employer_city = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=40,
                error="The employer city must have between 3 and 40 characters",
            ),
            validate.Regexp(
                r"^[a-zA-Z\s]+$",
                error="The employer city must only contain spaces and letters",
            ),
        ],
    )
    employer_country = fields.String(required=True)
    employer_province = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=50,
                error="The employer province must have between 3 and 50 characters",
            ),
            validate.Regexp(
                r"^[a-zA-Z\s]+", 
                error="The employer province must only contain spaces and letters",
            ),
        ],
    )
    employer_township = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=40,
                error="The employer township must have between 3 and 40 characters",
            ),
            validate.Regexp(
                r"^[a-zA-Z\s]+",
                error="The township must only contain spaces and letters",
            ),
        ],
    )
    employer_address = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=3,
                max=50,
                error="The employer address must have between 3 and 50 characters",
            ),
            validate.Regexp(
                r"[a-zA-Z0-9\s\.\-\/#()]+",
                error="The employer address entered is invalid, it must have only letters, numbers, spaces, and the following characters: ., -, /, #( )",
            ),
        ],
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
        m, d, y = value.split("-")
        m, d, y = int(m), int(d), int(y)
        birthdate_t = datetime.date(month=m, day=d, year=y)

        today = datetime.date.today()
        age = (
            today.year
            - birthdate_t.year
            - ((today.month, today.day) < (birthdate_t.month, birthdate_t.day))
        )

        if age < 18:
            raise ValidationError("The minimum age to register is 18 years")
        elif age > 100:
            raise ValidationError("The maximun age to register is 100 years")

    @validates_schema(skip_on_field_errors=True)
    def validate_phone_number(self, data, **kwargs):
        """
        Throws an exception if the phone number is not valid

        A phone number is valid if it is a valid number in the country entered.
        """
        # Get the country code from the country name
        country = pycountry.countries.search_fuzzy(data["country"])[0]
        iso_code = country.alpha_2

        # Validate the phone number using the country code
        phone_number = phonenumbers.parse(data["phone"], iso_code)
        is_valid = phonenumbers.is_valid_number(phone_number)

        if not is_valid:
            raise ValidationError("The phone number entered is invalid")

    @validates("country")
    def validate_country(self, value):
        country = pycountry.countries.search_fuzzy(value)[0]
        if country is None:
            raise ValidationError("The country entered is invalid")

    @validates_schema(skip_on_field_errors=True)
    def validate_employer_phone(self, data, **kwargs):
        """
        Throws an exception if the phone number is not valid

        A employer phone number is valid if it is a valid number in the country entered.
        """
        # Get the country code from the country name
        country = pycountry.countries.search_fuzzy(data["employer_country"])[0]
        iso_code = country.alpha_2

        # Validate the phone number using the country code
        phone_number = phonenumbers.parse(data["employer_phone"], iso_code)
        is_valid = phonenumbers.is_valid_number(phone_number)

        if not is_valid:
            raise ValidationError("The employer phone number entered is invalid")
>>>>>>> api-error-handling

    @validates("employer_country")
    def validate_employer_country(self, value):
        """

            Validates that a user's employer_country contains only letters.

            Throws an exception if employer country is not valid
        """
        country = pycountry.countries.search_fuzzy(value)[0]
        if country is None:
            raise ValidationError("The employer country entered is invalid")

class Update_Account_Holder_Schema(Create_Account_Holder_Schema):
    # User data
    login = fields.String(validate=validate.Length(min=4, max=20))
    password = fields.String(validate=validate.Length(min=6, max=20))
    name = fields.String(validate=validate.Length(min=2, max=20))
    lastname = fields.String(validate=validate.Length(min=2, max=20))
    user_type = fields.String(validate=validate.Length(min=4, max=20))
    role_id = fields.Integer()
    
    # Account holder fields
    id_number = fields.String()
    gender = fields.String()
    civil_status = fields.String()
    birthdate = fields.String()
    phone = fields.String()
    nationality = fields.String()
    street = fields.String()
    sector = fields.String()
    city = fields.String()
    country = fields.String()
    province = fields.String()
    township = fields.String()
    address = fields.String()
    employer_name = fields.String()
    employer_rif = fields.String()
    employer_phone = fields.String()
    employer_city = fields.String()
    employer_country = fields.String()
    employer_province = fields.String()
    employer_township = fields.String()
    employer_address = fields.String()
    user_id = fields.Integer()
    

    class Meta:
        exclude = ("id",)


class Get_Account_Holder_Schema(Generic_Get_Schema):
    
    user_id = fields.Integer()
    id_number = fields.String()
    gender = fields.String()
    civil_status = fields.String()
    birthdate = fields.String()
    phone = fields.String()
    nationality = fields.String()
    street = fields.String()
    sector = fields.String()
    city = fields.String()
    country = fields.String()
    province = fields.String()
    township = fields.String()
    address = fields.String()
    employer_name = fields.String()
    employer_rif = fields.String()
    employer_phone = fields.String()
    employer_city = fields.String()
    employer_country = fields.String()
    employer_province = fields.String()
    employer_township = fields.String()
    employer_address = fields.String()
    sort_by = fields.Str(
        load_default=None,
        validate=validate.OneOf(
            [
                'id',
                'user_id',
                'id_number',
                'gender',
                'civil_status',
                'birthdate',
                'phone',
                'nacionality',
                'street',
                'sector',
                'city',
                'country',
                'province',
                'township',
                'address',
                'employer_name',
                'employer_rif',
                'employer_phone',
                'employer_city',
                'employer_country',
                'employer_province',
                'employer_township',
                'employer_address',
            ]
        ),
    )
