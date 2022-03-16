from marshmallow import fields, validate

from main.schemas.base import BaseSchema


class LoadCategorySchema(BaseSchema):
    name = fields.String(validate=validate.Length(max=50), required=True)
