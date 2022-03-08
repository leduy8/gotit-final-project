from typing import Dict, List

from main import db
from main.models.category import CategoryModel


def find_by_name(name: str) -> CategoryModel:
    category = CategoryModel.query.filter_by(name=name).first()

    if not category:
        return None

    return category


def get_category_data(category: CategoryModel, user_id: int) -> Dict:
    return {
        'id': category.id,
        'name': category.name,
        'created': category.created,
        'updated': category.updated,
        'is_owner': category.user_id == user_id
    }


def get_all(params: Dict, user_id: int) -> List[CategoryModel]:
    categories = CategoryModel.query.paginate(
        params['page'], params['items_per_page'], False)

    categories = [get_category_data(category, user_id) for category in categories.items]

    return {
        'categories': categories,
        'page': params['page'],
        'items_per_page': params['items_per_page'],
        'total_items': params['total_items']
    }


def get_count():
    return CategoryModel.query.count()


def get_by_id(id, user_id):
    category = CategoryModel.query.filter_by(id=id).first()

    if not category:
        return None

    return get_category_data(category, user_id)


def create(data: Dict, user_id) -> CategoryModel:
    category = CategoryModel(name=data['name'], user_id=user_id)

    db.session.add(category)
    db.session.commit()

    return category


def update(data, id) -> CategoryModel:
    if CategoryModel.query.filter_by(name=data['name']).first():
        return None

    category = CategoryModel.query.filter_by(id=id).first()

    category.name = data['name']

    db.session.commit()

    return category


def delete(id):
    category = CategoryModel.query.filter_by(id=id).first()

    if not category:
        return None

    db.session.delete(category)
    db.session.commit()
