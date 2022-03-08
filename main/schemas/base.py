from flask import jsonify
from marshmallow import EXCLUDE, Schema, fields, validate


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))


class PaginationSchema(BaseSchema):
    items_per_page = fields.Integer(
        validate=validate.Range(min=1)
    )
    page = fields.Integer(
        validate=validate.Range(min=1)
    )
    total_items = fields.Integer()
