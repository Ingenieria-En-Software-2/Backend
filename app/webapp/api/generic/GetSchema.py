"""
A generic schema for accepting pagination parameters in Get requests. 
It is necessary to implement the 'sort by' field in the classes that inherit from this schema
"""

from marshmallow import Schema, fields, validate


class Generic_Get_Schema(Schema):
    page_number = fields.Integer(load_default=1, validate=validate.Range(min=1))
    page_size = fields.Integer(load_default=10, validate=validate.Range(min=1))
    sort_order = fields.Str(
        load_default="asc", validate=validate.OneOf(["asc", "desc"])
    )
    # sort_by must be implemented in the class that inherits from this schema
