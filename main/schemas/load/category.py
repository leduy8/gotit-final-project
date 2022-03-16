from marshmallow import fields

from main.schemas.base import BaseSchema


class LoadCategorySchema(BaseSchema):
    name = fields.String()
