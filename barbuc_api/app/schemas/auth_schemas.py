from bson import ObjectId
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from marshmallow import Schema, fields, pre_load, pre_dump
from marshmallow import validates_schema, ValidationError
from marshmallow.validate import Range

class LoginParamsSchema(Schema):
    email = fields.String(metadata={"description": "Email of the login"}, required=True)
    password = fields.String(metadata={"description": "Password of the login"}, required=True)

    class Meta:
        description = "Login details"
        ordered = True


class LoginResponseSchema(Schema):
    token = fields.String(metadata={"description": "Token of the user"})

    class Meta:
        description = "Token of the user"
        ordered = True


class LogoutResponseSchema(Schema):
    msg = fields.String(metadata={"description": "Message of logout"})

    class Meta:
        description = "Logout details"
        ordered = True