from bson import ObjectId
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from marshmallow import Schema, fields, pre_load, pre_dump
from marshmallow import validates_schema, ValidationError
from marshmallow.validate import Range

from ..models.user import User, USER_ID_MAX_VAL

class UserSchema(Schema):
    user_id = fields.Integer(
        attribute='user_id',
        validate=Range(min=0, min_inclusive=False, max=USER_ID_MAX_VAL, max_inclusive=False),
        metadata={"description": "Unique user identifier"}
    )
    name = fields.String(metadata={"exclude_if_null": True, "description": "Name of the user"})
    email = fields.String(metadata={"exclude_if_null": True, "description": "Email of the user"})

    _last_login = fields.String(
        format="date-time",
        allow_none=True,
        data="last_login",
        metadata={"exclude_if_null": True, "description": "Last login date of the user"}
    )
    
    _creation_time = fields.String(
        format="date-time",
        allow_none=True,
        data="creation_time",
        metadata={"exclude_if_null": True, "description": "User creation time"}
    )

    _update_time = fields.String(
        format="date-time",
        allow_none=True,
        data="update_time",
        metadata={"exclude_if_null": True, "description": "Last user update time"}
    )

    class Meta:
        ordered = True
        description = "User informations."


class UserResponseSchema(Schema):
    action = fields.String()
    user = fields.Nested(UserSchema)

    class Meta:
        ordered = True
        description = "Create/Update/Delete a user."


class GetUsersListSchema(Schema):
    users = fields.Nested(UserSchema, many=True)

    class Meta:
        description = "List of users."
        ordered = True


class InputCreateUserSchema(Schema):
    email = fields.String(metadata={"description": "Email of the user"}, required=True)
    password = fields.String(metadata={"description": "Password of the user"}, required=True)
    name = fields.String(metadata={"description": "Name of the user"}, required=True)

    class Meta:
        description = "Input informations need to create user."
        ordered = True


class InputUpdateUserSchema(Schema):
    email = fields.String(metadata={"description": "New email of the user"}, required=False)
    password = fields.String(metadata={"description": "New password of the user"}, required=False)
    name = fields.String(metadata={"description": "New name of the user"}, required=False)

    class Meta:
        description = "New user information"
        ordered = True


class InputUpdateUserSchema(Schema):
    email = fields.String(metadata={"description": "New email of the user"}, required=False)
    password = fields.String(metadata={"description": "New password of the user"}, required=False)
    name = fields.String(metadata={"description": "New name of the user"}, required=False)
    scopes = fields.List(
        fields.String,
        metadata={"description": "New scopes of the user"},
        required=False
    )

    class Meta:
        description = "New user information"
        ordered = True
