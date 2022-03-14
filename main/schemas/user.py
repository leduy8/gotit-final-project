from marshmallow import fields, validate

from main.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(validate=validate.Length(max=254), required=True)
    password = fields.String(
        load_only=True, required=True, validate=validate.Length(min=6, max=32)
    )
    salt = fields.String(dump_only=True)
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)
