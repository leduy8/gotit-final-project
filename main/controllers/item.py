from typing import Dict

from flask import jsonify

from main import app
from main.commons.decorators import authenticate_user, pass_data
from main.commons.exceptions import BadRequest, Forbidden, NotFound
from main.engines import category as category_engine
from main.engines import item as item_engine
from main.models.item import ItemModel
from main.schemas.dump.item import DumpItemSchema
from main.schemas.load.item import LoadItemSchema
from main.schemas.paginate import ItemPaginationSchema


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


@app.post("/items")
@authenticate_user()
@pass_data(LoadItemSchema)
def create_item(data, user_id):
    if not category_engine.find_category_by_id(data["category_id"]):
        raise BadRequest(error_message="Invalid category id")

    item = item_engine.create_item(data, user_id)

    return DumpItemSchema().jsonify(item)


@app.get("/items")
@authenticate_user(required=False)
@pass_data(ItemPaginationSchema)
def get_items(data, user_id):
    if "category_id" in data:
        if not category_engine.find_category_by_id(data["category_id"]):
            raise BadRequest(error_message="Invalid category id")

    items, total_items = item_engine.get_items(data)

    return jsonify(
        {
            "items": [get_item_data(item, user_id) for item in items],
            "page": data["page"],
            "items_per_page": data["items_per_page"],
            "total_items": total_items,
        }
    )


@app.get("/items/<int:id>")
@authenticate_user(required=False)
def get_item_by_id(user_id, id):
    item = item_engine.find_item_by_id(id)

    if not item:
        raise NotFound(error_message="Item not found")

    return DumpItemSchema().jsonify(item)


@app.put("/items/<int:id>")
@authenticate_user()
@pass_data(LoadItemSchema)
def update_item_by_id(data, user_id, id):
    item = item_engine.find_item_by_id(id)

    if not item:
        raise NotFound(error_message="Item not found")

    if item.user_id != user_id:
        raise Forbidden(
            error_message="User doesn't have permission to update this item"
        )

    if not category_engine.find_category_by_id(data["category_id"]):
        raise BadRequest(error_message="Invalid category id")

    updated_item = item_engine.update_item(data, item)

    return DumpItemSchema().jsonify(updated_item)


@app.delete("/items/<int:id>")
@authenticate_user()
def delete_item_by_id(user_id, id):
    item = item_engine.find_item_by_id(id)

    if not item:
        raise NotFound(error_message="Item not found")

    if item.user_id != user_id:
        raise Forbidden(
            error_message="User doesn't have permission to delete this item"
        )

    item_engine.delete_item(item)

    return jsonify({})
