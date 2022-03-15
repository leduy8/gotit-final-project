from typing import Dict, List

from main import db
from main.models.item import ItemModel


def get_item_count() -> int:
    return ItemModel.query.count()


def get_items(params: Dict) -> List[ItemModel]:
    items = ItemModel.query.paginate(params["page"], params["items_per_page"], False)

    items = [item for item in items.items]

    return items


def find_item_by_id(id) -> Dict:
    return ItemModel.query.filter_by(id=id).first()


def create_item(data: Dict, user_id) -> ItemModel:
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


def update_item(data, id) -> ItemModel:
    item = ItemModel.query.filter_by(id=id).first()

    if "name" in data:
        item.name = data["name"]

    if "description" in data:
        item.description = data["description"]

    if "category_id" in data:
        item.category_id = data["category_id"]

    db.session.commit()

    return item


def delete_item(id):
    item = ItemModel.query.filter_by(id=id).first()

    if not item:
        return None

    db.session.delete(item)
    db.session.commit()
