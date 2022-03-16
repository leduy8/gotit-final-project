from marshmallow import fields

from main.schemas.base import BaseSchema


class DumpCategorySchema(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    user_id = fields.Integer()
    created = fields.DateTime()
    updated = fields.DateTime()
