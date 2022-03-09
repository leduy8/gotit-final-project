from typing import Dict, List

from main import db
from main.models.item import ItemModel


def get_count() -> int:
    return ItemModel.query.count()


def get_item_data(item: ItemModel, user_id: int) -> Dict:
    return {
        'id': item.id,
        'name': item.name,
        'description': item.description or None,
        'created': item.created,
        'updated': item.updated,
        'is_owner': item.user_id == user_id,
        'category_id': item.category_id
    }


def get_all(params: Dict, user_id: int) -> List[ItemModel]:
    items = ItemModel.query.paginate(
        params['page'],
        params['items_per_page'],
        False
    )

    items = [get_item_data(item, user_id) for item in items.items]

    return {
        'items': items,
        'page': params['page'],
        'items_per_page': params['items_per_page'],
        'total_items': params['total_items']
    }


def get_by_id(id, user_id) -> Dict:
    item = ItemModel.query.filter_by(id=id).first()

    if not item:
        return None

    return get_item_data(item, user_id)


def create(data: Dict, user_id) -> ItemModel:
    item = ItemModel(
        name=data['name'],
        user_id=user_id,
        category_id=data['category_id'],
        description=data['description'] if 'description' in data else None
    )

    db.session.add(item)
    db.session.commit()

    return item


def update(data, id) -> ItemModel:
    if ItemModel.query.filter_by(name=data['name']).first():
        return None

    item = ItemModel.query.filter_by(id=id).first()

    item.name = data['name']
    item.description = data['description'] if 'description' in data else item.description

    db.session.commit()

    return item


def delete(id):
    item = ItemModel.query.filter_by(id=id).first()

    if not item:
        return None

    db.session.delete(item)
    db.session.commit()
