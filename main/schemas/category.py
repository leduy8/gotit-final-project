from marshmallow import fields, validate

from main.schemas.base import BaseSchema


class CategorySchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        validate=validate.Length(max=50),
        required=True
    )
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)
