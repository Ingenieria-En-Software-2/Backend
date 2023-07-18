"""
Module for defining schemas for the Role model.
"""

from marshmallow import Schema, fields, validate
from ...api.generic.GetSchema import Generic_Get_Schema


class Wallet_Schema(Schema):
    id = fields.Integer()
    description = fields.Str(validate=validate.Length(min=1), required=True)


class Update_Wallet_Schema(Schema):
    description = fields.Str(validate=validate.Length(min=1))


class Get_Wallet_Schema(Generic_Get_Schema):
    id = fields.Integer()
    description = fields.Str()
    sort_by = fields.Str(
        load_default=None, validate=validate.OneOf(["id", "description"])
    )
