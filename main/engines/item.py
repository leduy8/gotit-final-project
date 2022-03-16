from typing import Dict, List

from main import db
from main.models.item import ItemModel


def get_item_count() -> int:
    return ItemModel.query.count()


def get_items(params: Dict) -> List[object]:
    if "category_id" in params:
        items = ItemModel.query.filter_by(category_id=params["category_id"]).paginate(
            params["page"], params["items_per_page"], False
        )
    else:
        items = ItemModel.query.paginate(
            params["page"], params["items_per_page"], False
        )

    return [items.items, items.total]


def find_item_by_id(id: int) -> ItemModel:
    return ItemModel.query.get(id)


def create_item(data: Dict, user_id: int) -> ItemModel:
    item = ItemModel(
        name=data["name"],
        user_id=user_id,
        category_id=data["category_id"],
    )

    if "description" in data:
        item.description = data["description"]

    db.session.add(item)
    db.session.commit()

    return item


def update_item(data: Dict, item: ItemModel) -> ItemModel:
    item.name = data["name"]
    item.category_id = data["category_id"]

    if "description" in data:
        item.description = data["description"]

    db.session.commit()

    return item


def delete_item(item: ItemModel):
    db.session.delete(item)
    db.session.commit()
