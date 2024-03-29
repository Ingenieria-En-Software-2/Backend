"""
Module containing definitions of schemas for account holder management in the API.
"""

import datetime
import phonenumbers
import pycountry
import re
from ...api.user.schemas import Create_User_Schema
from ...api.account_holder.models import AccountHolder
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


class Create_Account_Holder_Schema(Create_User_Schema):
    # Override password
    password = fields.String(required=False, validate=validate.Length(min=6, max=20))
    user_id = fields.Integer()

    # Account holder fields
    id = fields.Integer()
    id_number = fields.String(required=True)
    gender = fields.String(required=True)
    civil_status = fields.String(required=True)
    birthdate = fields.String(required=True)
    phone = fields.String(required=True)
    nationality = fields.String(
        required=True,
        validate=validate.Length(
            min=3,
            max=30,
            error="La nacionalidad debe tener entre 3 y 30 caracteres",
        ),
    )
    street = fields.String(
        required=True,
        validate=validate.Length(
            min=3,
            max=50,
            error="La calle debe tener entre 3 y 50 caracteres",
        ),
    )
    sector = fields.String(
        required=True,
        allow_none=True,
        validate=validate.Length(
            min=3,
            max=50,
            error="El sector debe tener entre 3 y 50 caracteres",
        ),
    )
    city = fields.String(
        required=True,
        allow_none=True,
        validate=validate.Length(
            min=3,
            max=50,
            error="La ciudad debe tener entre 3 y 50 caracteres",
        ),
    )
    country = fields.String(required=True)
    province = fields.String(
        required=True,
        allow_none=True,
        validate=validate.Length(
            min=3,
            max=20,
            error="La provincia debe tener entre 3 y 20 caracteres",
        ),
    )
    township = fields.String(
        required=True,
        validate=validate.Length(
            min=3,
            max=20,
            error="El municipio debe tener entre 3 y 20 caracteres",
        ),
    )
    address = fields.String(
        required=True,
        validate=validate.Length(
            min=3,
            max=150,
            error="La dirección debe tener entre 3 y 150 caracteres",
        ),
    )
    employer_name = fields.String(
        required=True,
        validate=validate.Length(
            min=3,
            max=50,
            error="El nombre del empleador debe tener entre 3 y 50 caracteres",
        ),
    )
    employer_rif = fields.String(required=True)
    employer_phone = fields.String(required=True)
    employer_city = fields.String(
        required=True,
        allow_none=True,
        validate=validate.Length(
            min=3,
            max=50,
            error="La ciudad del empleador debe tener entre 3 y 50 caracteres",
        ),
    )
    employer_country = fields.String(required=True)
    employer_province = fields.String(
        required=True,
        allow_none=True,
        validate=validate.Length(
            min=3,
            max=20,
            error="La provincia del empleador debe tener entre 3 y 20 caracteres",
        ),
    )
    employer_township = fields.String(
        required=True,
        validate=validate.Length(
            min=3,
            max=20,
            error="El municipio del empleador debe tener entre 3 y 20 caracteres",
        ),
    )
    employer_address = fields.String(
        required=True,
        validate=validate.Length(
            min=3,
            max=150,
            error="La dirección del empleador debe tener entre 3 y 150 caracteres",
        ),
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
                "El número de cédula ingresado es inválido, debe tener el "
                + "formato <Tipo>-<número> Posibles valores para tipo: V,J,G,E,C "
                + "y número debe tener entre 7 y 8 dígitos"
            )

    @validates("gender")
    def validate_gender(self, value):
        """
        Throws an exception if the gender is not valid

        A gender is valid if it is one of the following: M, F, O
        """
        regex = r"^[M|F|O]$"
        if not re.fullmatch(regex, value):
            raise ValidationError("El género debe ser uno de los siguientes: M, F, O")

    @validates("civil_status")
    def validate_civil_status(self, value):
        """
        Throws an exception if the civil status is not valid

        A civil status is valid if it is one of the following: S, C, D, V
        """
        regex = r"^[S|C|D|V]$"
        if not re.fullmatch(regex, value):
            raise ValidationError(
                "El estado civil debe ser uno de los siguientes: S, C, D, V"
            )

    @validates("birthdate")
    def validate_birthdate(self, value):
        """
        Throws an exception if the birthdate is not valid

        A valid birthdate is:
         - A string with the format MM-DD-YYYY
         - Minimum age is 18 years.
         - Maximum age is 100 years.
        """
        regex = r"^\d{2}-\d{2}-\d{4}$"
        if not re.fullmatch(regex, value):
            raise ValidationError(
                "La fecha de nacimiento debe tener el formato MM-DD-YYYY"
            )

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
            raise ValidationError("La edad mínima para registrarse es 18 años")
        elif age > 100:
            raise ValidationError("La edad máxima para registrarse es 100 años")

    @validates("nationality")
    def validate_nationality(self, value):
        """
        Throws an exception if the nationality es not valid

        A nationality is valid if only contains letters
        """
        regex = r"^[a-zA-Z\sáéíóúÁÉÍÓÚñÑüÜ]+"
        if not re.fullmatch(regex, value):
            raise ValidationError(
                "La nacionalidad debe contener solo letras y espacios"
            )

    @validates("street")
    def validate_street(self, value):
        """
        Throws an exception if the street is not valid

        A street is valid if it only contains letters, numbers and the
        following characters: ., _, -, /, #, (, )
        """
        regex = r"^[a-zA-Z0-9\sáéíóúÁÉÍÓÚñÑüÜ\.\-\/#()]+$"
        if not re.fullmatch(regex, value):
            raise ValidationError(
                "La calle debe contener solo letras, espacios, números y los "
                + "caracteres ., _, -, /, #, (, )"
            )

    @validates("sector")
    def validate_sector(self, value):
        """
        Throws an exception if the sector is not valid

        A sector is valid if it only contains letters, numbers and the
        following characters: ., _, -, /, #, (, )
        """
        # If the sector is None, it is not validated
        if value is not None:
            regex = r"^[a-zA-Z0-9\sáéíóúÁÉÍÓÚñÑüÜ\.\-\/#()]+$"
            if not re.fullmatch(regex, value):
                raise ValidationError(
                    "El sector debe contener solo letras, espacios, números y "
                    + "los caracteres ., _, -, /, #, (, )"
                )

    @validates("city")
    def validate_city(self, value):
        """
        Throws an exception if the city is not valid

        A city is valid if it only contains letters and spaces
        """
        # If the city is None, it is not validated
        if value is not None:
            regex = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$"
            if not re.fullmatch(regex, value):
                raise ValidationError("La ciudad debe contener solo letras y espacios")

    @validates("country")
    def validate_country(self, value):
        country = pycountry.countries.search_fuzzy(value)[0]
        if country is None:
            raise ValidationError("El país ingresado no es válido")

    @validates("province")
    def validate_province(self, value):
        """
        Throws an exception if the province is not valid

        A province is valid if it only contains letters and spaces
        """
        # If the province is None, it is not validated
        if value is not None:
            regex = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$"
            if not re.fullmatch(regex, value):
                raise ValidationError(
                    "La provincia debe contener solo letras y espacios"
                )

    @validates("township")
    def validate_township(self, value):
        """
        Throws an exception if the township is not valid

        A township is valid if it only contains letters and spaces
        """
        regex = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$"
        if not re.fullmatch(regex, value):
            raise ValidationError("El municipio debe contener solo letras y espacios")

    @validates("address")
    def validate_address(self, value):
        """
        Throws an exception if the address is not valid

        An address is valid if it only contains letters, numbers and the
        following characters: ., _, -, /, #, (, )
        """
        regex = r"^[a-zA-Z0-9\sáéíóúÁÉÍÓÚñÑüÜ\.\-\/#()]+$"
        if not re.fullmatch(regex, value):
            raise ValidationError(
                "La dirección debe contener solo letras, espacios, números y "
                + "los caracteres ., _, -, /, #, (, )"
            )

    @validates("employer_name")
    def validate_employer_name(self, value):
        """
        Throws an exception if the employer name is not valid

        An employer name is valid if it only contains letters and spaces
        """
        regex = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$"
        if not re.fullmatch(regex, value):
            raise ValidationError(
                "El nombre del empleador debe contener solo letras y espacios"
            )

    @validates("employer_rif")
    def validate_employer_rif(self, value):
        """
        Throws an exception if the employer RIF is not valid

        An employer RIF is valid if it has the following format:
        <letter>-<number>-<digit> where:
         - letter can be V, E, J, P, G
         - number must have between 7 and 8 digits
         - digit must be between 0 and 9
        """
        regex = r"^[V|E|J|P|G|v|e|j|p|g]-\d{7,8}-\d$"
        if not re.fullmatch(regex, value):
            raise ValidationError(
                "El RIF del empleador debe tener el formato"
                + " <letra>-<número>-<dígito> Letras posibles: V, E, J, P, G,"
                + " números deben tener entre 7 y 8 dígitos y el dígito debe"
                + " estar entre 0 y 9"
            )

    @validates("employer_city")
    def validate_employer_city(self, value):
        """
        Throws an exception if the employer city is not valid

        An employer city is valid if it only contains letters and spaces
        """
        # If the employer city is None, it is not validated
        if value is not None:
            regex = r"^[a-zA-Z\sáéíóúÁÉÍÓÚñÑüÜ]+$"
            if not re.fullmatch(regex, value):
                raise ValidationError(
                    "La ciudad del empleador debe contener solo letras y " + "espacios"
                )

    @validates("employer_country")
    def validate_employer_country(self, value):
        """
        Validates that a user's employer_country contains only letters.
        Throws an exception if employer country is not valid
        """
        country = pycountry.countries.search_fuzzy(value)[0]
        if country is None:
            raise ValidationError("El país del empleador es inválido")

    @validates("employer_province")
    def validate_employer_province(self, value):
        """
        Throws an exception if the employer province is not valid

        An employer province is valid if it only contains letters and spaces
        """
        # If the employer province is None, it is not validated
        if value is not None:
            regex = r"^[a-zA-Z\sáéíóúÁÉÍÓÚñÑüÜ]+$"
            if not re.fullmatch(regex, value):
                raise ValidationError(
                    "La provincia del empleador debe contener solo letras y "
                    + "espacios"
                )

    @validates("employer_township")
    def validate_employer_township(self, value):
        """
        Throws an exception if the employer township is not valid

        An employer township is valid if it only contains letters and spaces
        """
        regex = r"^[a-zA-Z\sáéíóúÁÉÍÓÚñÑüÜ]+$"
        if not re.fullmatch(regex, value):
            raise ValidationError(
                "El municipio del empleador debe contener solo letras y " + "espacios"
            )

    @validates("employer_address")
    def validate_employer_address(self, value):
        """
        Throws an exception if the employer address is not valid

        An employer address is valid if it only contains letters, numbers and
        the following characters: ., _, -, /, #, (, )
        """
        regex = r"^[a-zA-Z0-9\sáéíóúÁÉÍÓÚñÑüÜ\.\-\/#()]+$"
        if not re.fullmatch(regex, value):
            raise ValidationError(
                "La dirección del empleador debe contener solo letras, "
                + "espacios, números y los caracteres ., _, -, /, #, (, )"
            )

    @validates_schema(skip_on_field_errors=True)
    def validate_phone_number(self, data, **kwargs):
        """
        Throws an exception if the phone number is not valid

        A phone number is valid if it is a valid number in the country entered.
        """
        # If the phone number is entered but not the country, get the country
        if "phone" in data and "country" not in data:
            # Get the country of the user
            istance = AccountHolder.query.filter_by(id=data["id"]).first()
            country = pycountry.countries.search_fuzzy(istance.country)[0]
            iso_code = country.alpha_2

            # Validate the phone number using the country code
            phone_number = phonenumbers.parse(data["phone"], iso_code)
            is_valid = phonenumbers.is_valid_number(phone_number)

            if not is_valid:
                raise ValidationError("El número de teléfono ingresado es inválido")
        # If the phone number and country is entered, validate the phone number
        elif "phone" in data and "country" in data:
            # Get the country code from the country name
            country = pycountry.countries.search_fuzzy(data["country"])[0]
            iso_code = country.alpha_2

            # Validate the phone number using the country code
            phone_number = phonenumbers.parse(data["phone"], iso_code)
            is_valid = phonenumbers.is_valid_number(phone_number)

            if not is_valid:
                raise ValidationError("El número de teléfono ingresado es inválido")

    @validates_schema(skip_on_field_errors=True)
    def validate_employer_phone(self, data, **kwargs):
        """
        Throws an exception if the phone number is not valid

        A employer phone number is valid if it is a valid number in the country entered.
        """
        # If the phone number is entered but not the country, get the country
        if "employer_phone" in data and "employer_country" not in data:
            # Get the country of the user
            istance = AccountHolder.query.filter_by(id=data["id"]).first()
            country = pycountry.countries.search_fuzzy(istance.country)[0]
            iso_code = country.alpha_2

            # Validate the phone number using the country code
            phone_number = phonenumbers.parse(data["employer_phone"], iso_code)
            is_valid = phonenumbers.is_valid_number(phone_number)

            if not is_valid:
                raise ValidationError(
                    "El número de teléfono del empleador ingresado es inválido"
                )
        # If the phone number or country is not entered, skip the validation
        elif "employer_phone" in data and "employer_country" in data:
            # Get the country code from the country name
            country = pycountry.countries.search_fuzzy(data["employer_country"])[0]
            iso_code = country.alpha_2

            # Validate the phone number using the country code
            phone_number = phonenumbers.parse(data["employer_phone"], iso_code)
            is_valid = phonenumbers.is_valid_number(phone_number)

            if not is_valid:
                raise ValidationError(
                    "El número de teléfono del empleador ingresado es inválido"
                )

    @post_load
    def convert_birthdate(self, data, **kwargs):
        """
        Convert the birthdate to a date type
        """
        # If the birthdate is not entered, skip the validation
        if "birthdate" in data:
            m, d, y = data["birthdate"].split("-")
            m, d, y = int(m), int(d), int(y)
            data["birthdate"] = datetime.date(month=m, day=d, year=y)
        return data

    @post_load
    def formated_id_number(self, data, **kwargs):
        """
        Returns the id number transformed to a standard format:
         - Begins with a capital letter.
         - Followed by a dash and 7 or 8 digits.
        """
        # If the id number is not entered, skip the validation
        if "id_number" in data:
            # Remove spaces and dots from the number
            table = str.maketrans("", "", ". ")
            id_number = data["id_number"].translate(table)

            # To upper case
            id_number = id_number.upper()
            data["id_number"] = id_number
        return data


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
    nationality = fields.String(validate=validate.Length(min=3, max=30))
    street = fields.String(validate=validate.Length(min=3, max=50))
    sector = fields.String(validate=validate.Length(min=3, max=50), allow_none=True)
    city = fields.String(validate=validate.Length(min=3, max=50), allow_none=True)
    country = fields.String()
    province = fields.String(validate=validate.Length(min=2, max=20), allow_none=True)
    township = fields.String(validate=validate.Length(min=3, max=20))
    address = fields.String(validate=validate.Length(min=3, max=150))
    employer_name = fields.String(validate=validate.Length(min=4, max=50))
    employer_rif = fields.String()
    employer_phone = fields.String()
    employer_city = fields.String(
        validate=validate.Length(min=3, max=50), allow_none=True
    )
    employer_country = fields.String(validate=validate.Length(min=3, max=20))
    employer_province = fields.String(
        validate=validate.Length(min=3, max=20), allow_none=True
    )
    employer_township = fields.String(validate=validate.Length(min=3, max=20))
    employer_address = fields.String(validate=validate.Length(min=3, max=150))
    user_id = fields.Integer()


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
                "id",
                "user_id",
                "id_number",
                "gender",
                "civil_status",
                "birthdate",
                "phone",
                "nationality",
                "street",
                "sector",
                "city",
                "country",
                "province",
                "township",
                "address",
                "employer_name",
                "employer_rif",
                "employer_phone",
                "employer_city",
                "employer_country",
                "employer_province",
                "employer_township",
                "employer_address",
            ]
        ),
    )
