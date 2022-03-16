from marshmallow import fields, validate

from main.schemas.base import BaseSchema


class LoadItemSchema(BaseSchema):
    name = fields.String(validate=validate.Length(max=80), required=True)
    description = fields.String(validate=validate.Length(max=200))
    category_id = fields.Integer(
        validate=validate.Range(min=1),
        required=True,
    )
