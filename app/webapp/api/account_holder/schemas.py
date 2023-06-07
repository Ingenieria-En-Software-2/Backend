"""
Module containing definitions of schemas for account holder management in the API.
"""

from marshmallow import Schema, fields, validate, validates, ValidationError
from webapp.api.generic.GetSchema import Generic_Get_Schema
import re

# Definition of the schemas for validation of account holder data


class Create_Account_Holder_Schema(Schema):
    pass


class Update_Account_Holder_Schema(Create_Account_Holder_Schema):
    pass


class Get_Account_Holder_Schema(Generic_Get_Schema):
    pass
