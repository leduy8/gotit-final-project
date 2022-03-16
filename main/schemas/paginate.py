from marshmallow import fields, validate

from main import config
from main.schemas.base import PaginationSchema


class CategoryPaginationSchema(PaginationSchema):
    items_per_page = fields.Integer(
        missing=config.CATEGORIES_PER_PAGE, validate=validate.Range(min=1)
    )


class ItemPaginationSchema(PaginationSchema):
    items_per_page = fields.Integer(
        missing=config.ITEMS_PER_PAGE, validate=validate.Range(min=1)
    )
