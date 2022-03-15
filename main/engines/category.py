from typing import Dict, List

from main import db
from main.models.category import CategoryModel


def find_category_by_name(name: str) -> CategoryModel:
    return CategoryModel.query.filter_by(name=name).first()


def find_category_by_id(id) -> Dict:
    return CategoryModel.query.filter_by(id=id).first()


def get_category_count() -> int:
    return CategoryModel.query.count()


def get_categories(params: Dict) -> List[CategoryModel]:
    categories = CategoryModel.query.paginate(
        params["page"], params["items_per_page"], False
    )

    categories = [category for category in categories.items]

    return categories


def create_category(data: Dict, user_id) -> CategoryModel:
    category = CategoryModel(name=data["name"], user_id=user_id)

    db.session.add(category)
    db.session.commit()

    return category


def update_category(data, id) -> CategoryModel:
    category = CategoryModel.query.filter_by(id=id).first()

    category.name = data["name"]

    db.session.commit()

    return category


def delete_category(id):
    category = CategoryModel.query.filter_by(id=id).first()

    if not category:
        return None

    db.session.delete(category)
    db.session.commit()
