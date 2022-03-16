from marshmallow import fields, validate

from main.schemas.base import BaseSchema


class LoadUserSchema(BaseSchema):
    email = fields.Email(validate=validate.Length(max=254), required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=32))
