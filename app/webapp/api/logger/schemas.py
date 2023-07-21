"""
Module containing definitions of schemas for account holder management in the API.
"""

import re
from ...api.user.schemas import Create_User_Schema
from ...api.user_account.models import UserAccount
from ...auth.models import User
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


class Create_Log_Event_Schema(Schema):
    # Account holder fields
    id = fields.Integer()
    user_id = fields.Integer(required=True)
    description = fields.Str(required=True)
    occurrence_time = fields.DateTime()


class Update_Log_Event_Schema(Create_Log_Event_Schema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_obj in self.fields.items():
            field_obj.required = False

    class Meta:
        exclude = ("id",)


class Get_Log_Event_Schema(Generic_Get_Schema, Update_Log_Event_Schema):
    sort_by = fields.String(
        load_default="id",
        validate=validate.OneOf(
            ["id", "user_id", "description", "occurrence_time"],
            error="El campo sort_by solo puede tomar los valores id, user_id, account_number o account_type_id",
        ),
    )

    class Meta:
        pass
