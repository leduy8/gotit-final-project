from marshmallow import fields

from main.schemas.base import BaseSchema


class DumpItemSchema(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    created = fields.DateTime()
    updated = fields.DateTime()
    user_id = fields.Integer()
    category_id = fields.Integer()
