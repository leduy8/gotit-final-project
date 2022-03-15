from typing import Dict, List

from flask import jsonify

from main import app
from main.commons.decorators import authorize_user, validate_request
from main.commons.exceptions import BadRequest, Forbidden, NotFound
from main.engines import category as category_engine
from main.engines import item as item_engine
from main.models.item import ItemModel
from main.schemas.base import PaginationSchema
from main.schemas.item import ItemSchema


def get_item_data(item: ItemModel, user_id: int) -> Dict:
    return {
        "id": item.id,
        "name": item.name,
        "description": item.description or None,
        "created": item.created,
        "updated": item.updated,
        "is_owner": item.user_id == user_id,
        "category_id": item.category_id,
    }


def get_item_data_with_params_data(items: List[ItemModel], user_id, *args, **kwargs):
    return {
        "items": [get_item_data(item, user_id) for item in items],
        "page": kwargs["params"]["page"],
        "items_per_page": kwargs["params"]["items_per_page"],
        "total_items": kwargs["params"]["total_items"],
    }


@app.post("/items")
@authorize_user()
@validate_request(ItemSchema)
def create_item(data, user_id):
    item = item_engine.create_item(data, user_id)

    return ItemSchema().jsonify(item)


@app.get("/items")
@authorize_user(required=False)
@validate_request(PaginationSchema)
def get_items(data, user_id):
    params = {
        "page": 1,
        "items_per_page": app.config["ITEMS_PER_PAGE"],
        "total_items": item_engine.get_item_count(),
    }

    if "page" in data:
        params["page"] = data["page"]

    if "items_per_page" in data:
        params["items_per_page"] = data["items_per_page"]

    items = item_engine.get_items(params)

    return jsonify(
        get_item_data_with_params_data(items=items, user_id=user_id, params=params)
    )


@app.get("/items/<int:id>")
@authorize_user(required=False)
def get_item_by_id(user_id, id):
    item = item_engine.find_item_by_id(id)

    if not item:
        raise NotFound(error_message="Item not found")

    return ItemSchema().jsonify(item)


@app.put("/items/<int:id>")
@authorize_user()
@validate_request(ItemSchema)
def update_item_by_id(data, user_id, id):
    item = item_engine.find_item_by_id(id)

    if not item:
        raise NotFound(error_message="Item not found")

    if item.user_id != user_id:
        raise Forbidden(
            error_message="User doesn't have permission to update this item"
        )

    if "category_id" in data:
        if not category_engine.find_category_by_id(data["category_id"]):
            raise BadRequest(error_message="Invalid category id")

    updated_item = item_engine.update_item(data, id)

    return ItemSchema().jsonify(updated_item)


@app.delete("/items/<int:id>")
@authorize_user()
def delete_item_by_id(user_id, id):
    item = item_engine.find_item_by_id(id)

    if not item:
        raise NotFound(error_message="Item not found")

    if item.user_id != user_id:
        raise Forbidden(
            error_message="User doesn't have permission to delete this item"
        )

    item_engine.delete_item(id)

    return jsonify({})
