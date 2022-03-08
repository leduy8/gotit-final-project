from marshmallow import fields, validate

from main.schemas.base import BaseSchema


class IdSchema(BaseSchema):
    id = fields.Integer(
        validate=validate.Range(min=1)
    )
