"""
Módulo que contiene definiciones de esquemas para la gestión de Cuentahabientes en la
API.

Se definen tres esquemas: Create_Account_Holder_Schema, Update_Account_Holder_Schema y Get_Account_Holder_Schema, 
cada uno con sus respectivos argumentos y reglas de validación.
"""

from marshmallow import Schema, fields, validate, validates, ValidationError
from ..generic.GetSchema import Generic_Get_Schema
from ..user.schemas import Create_User_Schema
import re

# Definition of the schemas for validation of account holders data


class Create_Account_Holder_Schema(Create_User_Schema):
    # Override password
    password = fields.String(required=False, validate=validate.Length(min=6, max=20))
    user_id = fields.Integer()
    
    # Account holder fields
    id = fields.Integer()
    identification_document = fields.String(required=True, validate=validate.Length(min=4, max=20))
    gender = fields.String(required=True, validate=validate.Length(min=1, max=1))
    civil_status = fields.String(required=True, validate=validate.Length(min=4, max=20))
    birthdate = fields.String(required=True, validate=validate.Length(min=4, max=20))
    phone = fields.String(required=True, validate=validate.Length(min=4, max=20))
    nationality = fields.String(required=True, validate=validate.Length(min=4, max=20))
    street = fields.String(required=True, validate=validate.Length(min=4, max=50))
    sector = fields.String(required=True, validate=validate.Length(min=4, max=50))
    city = fields.String(required=True, validate=validate.Length(min=4, max=50))
    country = fields.String(required=True, validate=validate.Length(min=4, max=20))
    province = fields.String(required=True, validate=validate.Length(min=4, max=20))
    township = fields.String(required=True, validate=validate.Length(min=4, max=20))
    address = fields.String(required=True, validate=validate.Length(min=4, max=200))
    employer_name = fields.String(required=True, validate=validate.Length(min=4, max=50))
    employer_rif = fields.String(required=True, validate=validate.Length(min=4, max=20))
    employer_phone = fields.String(required=True, validate=validate.Length(min=4, max=20))
    employer_city = fields.String(required=True, validate=validate.Length(min=4, max=50))
    employer_country = fields.String(required=True, validate=validate.Length(min=4, max=20))
    employer_province = fields.String(required=True, validate=validate.Length(min=4, max=20))
    employer_township = fields.String(required=True, validate=validate.Length(min=4, max=20))
    employer_address = fields.String(required=True, validate=validate.Length(min=4, max=200))
    
    
    @validates("identification_document")
    def validate_identification_document(self, value):
        """
        Validates that a account holder's identification document contains the format <Type>-XXXXXXXXXX, 
        Throws a ValidationError exception in case the identification_document does
        not comply with the pattern.
        """

        regex = r"^[VJGE]-[0-9]{8,10}$"
        if not re.match(regex, value):
            raise ValidationError(
                "The identification document most be of the given format <Type>-<number> " +
                    "e.g. V-123456789 Posible values for type: V,J,G,E and number" +
                        " most have between 8 and 10 digits"
            )

    @validates("gender")
    def validate_gender(self, value):
        """
        Validates that a gender is M or F
        """
        regex = r"^[MF]{1}$"
        if not re.match(regex, value):
            raise ValidationError("The gender most be M or F")

    @validates("civil_status")
    def validate_civil_status(self, value):
        """
        Validates that a user's civil status contains only letters.
        Throws a ValidationError exception in case the last name does not
        comply with the pattern.
        """
        regex = r"^\w+$"
        if not re.match(regex, value):
            raise ValidationError("The civil status can only contain letters")
        
    @validates("birthdate")
    def validate_birthdate(self, value):
        """
        Validates date structure dd-mm-yyyy.
        Throws a ValidationError exception in case the the date does not
        comply with the pattern.
        """
        regex = r"^([0-2][0-9]|(3[01]))-(0\d|(1[012]))-\d{4}$"
        if not re.match(regex, value):
            raise ValidationError("The birthdate most be in format dd-mm-yyyy")
        
    @validates("phone")
    def validate_phone(self, value):
        """
        Validates phone format to contains 4 area code numbers and at least 7 digits.
        Throws a ValidationError exception in case that not
        comply with the pattern.
        """
        regex = r"^\d{4}-\d{7}$"
        if not re.match(regex, value):
            raise ValidationError("The phone most be in format XXXX-XXXXXXX")
        
    @validates("nationality")
    def validate_nationality(self, value):
        """
        Validates that a user's nationality contains only letters.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^\w+$"
        if not re.match(regex, value):
            raise ValidationError("The nationality can only contain letters")
        
    @validates("street")
    def validate_street(self, value):
        """
        Validates that a user's street address contains only letters.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^[\w\s\d]+$"
        if not re.match(regex, value):
            raise ValidationError("The street can only contain letters")
        
    @validates("sector")
    def validate_sector(self, value):
        """
        Validates that a user's sector contains only letters and spaces.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^[\w\s\d]+$"
        if not re.match(regex, value):
            raise ValidationError("The sector can only contain letters")

    @validates("city")
    def validate_city(self, value):
        """
        Validates that a user's city contains only letters.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^[\w\s]+$"
        if not re.match(regex, value):
            raise ValidationError("The city can only contain letters")

    @validates("country")
    def validate_country(self, value):
        """
        Validates that a user's country contains only letters.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^[\w\s]+$"
        if not re.match(regex, value):
            raise ValidationError("The country can only contain letters")

    @validates("province")
    def validate_province(self, value):
        """
        Validates that a user's province contains only letters.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^[\w\s]+$"
        if not re.match(regex, value):
            raise ValidationError("The province can only contain letters")

    @validates("township")
    def validate_township(self, value):
        """
        Validates that a user's township contains only letters.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^[\w\s]+$"
        if not re.match(regex, value):
            raise ValidationError("The township can only contain letters")
    
    @validates("address")
    def validate_address(self, value):
        """
        Validates that a user's address contains only letters.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^[\w\s\d]+$"
        if not re.match(regex, value):
            raise ValidationError("The address can only contain letters")


    @validates("employer_name")
    def validate_employer_name(self, value):
        """
        Validates that a user's employer_name contains only letters.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^[\w ]+$"
        if not re.match(regex, value):
            raise ValidationError("The employer_name can only contain letters")

    @validates("employer_rif")
    def validate_employer_rif(self, value):
        """
        Validates that a user's employer_rif contains only letters.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^[VJGE]-[0-9]{8,10}$"
        if not re.match(regex, value):
            raise ValidationError("The employer_rif can only contain letters")
    
    @validates("employer_phone")
    def validate_employer_phone(self, value):
        """
        Validates that a user's employer_phone contains only letters.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^\d{4}-\d{7}$"
        if not re.match(regex, value):
            raise ValidationError("The employer_phone can only contain letters")

    @validates("employer_city")
    def validate_employer_city(self, value):
        """
        Validates that a user's employer_city contains only letters.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^[\w\s]+$"
        if not re.match(regex, value):
            raise ValidationError("The employer_city can only contain letters")

    @validates("employer_country")
    def validate_employer_country(self, value):
        """
        Validates that a user's employer_country contains only letters.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^[\w\s]+$"
        if not re.match(regex, value):
            raise ValidationError("The employer_country can only contain letters")

    @validates("employer_province")
    def validate_employer_province(self, value):
        """
        Validates that a user's employer_province contains only letters.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^[\w\s]+$"
        if not re.match(regex, value):
            raise ValidationError("The employer_province can only contain letters")

    @validates("employer_township")
    def validate_employer_township(self, value):
        """
        Validates that a user's employer_township contains only letters.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^[\w\s]+$"
        if not re.match(regex, value):
            raise ValidationError("The employer_township can only contain letters")
    
    @validates("employer_address")
    def validate_employer_address(self, value):
        """
        Validates that a user's employer_address contains only letters.
        Throws a ValidationError exception in case does not
        comply with the pattern.
        """
        regex = r"^[\w\s\d]+$"
        if not re.match(regex, value):
            raise ValidationError("The employer_address can only contain letters")
        
        
class Update_Account_Holder_Schema(Create_Account_Holder_Schema):
    # User data
    login = fields.String(validate=validate.Length(min=4, max=20))
    password = fields.String(validate=validate.Length(min=6, max=20))
    name = fields.String(validate=validate.Length(min=2, max=20))
    lastname = fields.String(validate=validate.Length(min=2, max=20))
    user_type = fields.String(validate=validate.Length(min=4, max=20))
    role_id = fields.Integer()
    
    # Account holder fields
    identification_document = fields.String( validate=validate.Length(min=4, max=20))
    gender = fields.String( validate=validate.Length(min=1, max=1))
    civil_status = fields.String( validate=validate.Length(min=4, max=20))
    birthdate = fields.String( validate=validate.Length(min=4, max=20))
    phone = fields.String( validate=validate.Length(min=4, max=20))
    nationality = fields.String( validate=validate.Length(min=4, max=20))
    street = fields.String( validate=validate.Length(min=4, max=50))
    sector = fields.String( validate=validate.Length(min=4, max=50))
    city = fields.String( validate=validate.Length(min=4, max=50))
    country = fields.String( validate=validate.Length(min=4, max=20))
    province = fields.String( validate=validate.Length(min=4, max=20))
    township = fields.String( validate=validate.Length(min=4, max=20))
    address = fields.String( validate=validate.Length(min=4, max=200))
    employer_name = fields.String( validate=validate.Length(min=4, max=50))
    employer_rif = fields.String( validate=validate.Length(min=4, max=20))
    employer_phone = fields.String( validate=validate.Length(min=4, max=20))
    employer_city = fields.String( validate=validate.Length(min=4, max=50))
    employer_country = fields.String( validate=validate.Length(min=4, max=20))
    employer_province = fields.String( validate=validate.Length(min=4, max=20))
    employer_township = fields.String( validate=validate.Length(min=4, max=20))
    employer_address = fields.String( validate=validate.Length(min=4, max=200))
    user_id = fields.Integer()
    

    class Meta:
        exclude = ("id",)


class Get_Account_Holder_Schema(Generic_Get_Schema):
    
    user_id = fields.Integer()
    identification_document = fields.String()
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
                'identification_document',
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
