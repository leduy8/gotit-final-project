from marshmallow import fields, validate

from main.schemas.base import BaseSchema


class ItemSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        validate=validate.Length(max=80),
        required=True
    )
    description = fields.String(
        validate=validate.Length(max=200)
    )
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    category_id = fields.Integer(
        validate=validate.Range(min=1),
        required=True,
    )
