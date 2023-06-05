from marshmallow import Schema, fields, validate

class Generic_Get_Schema(Schema):
    page_number = fields.Integer(load_default=1, validate=validate.Range(min=1))
    page_size = fields.Integer(load_default=10, validate=validate.Range(min=1))
    sort_order = fields.Str(load_default='asc', validate=validate.OneOf(['asc', 'desc']))


