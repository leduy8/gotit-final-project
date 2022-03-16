from typing import Dict, List

from main import db
from main.models.category import CategoryModel


def find_category_by_name(name: str) -> CategoryModel:
    return CategoryModel.query.filter_by(name=name).first()


def find_category_by_id(id: int) -> CategoryModel:
    return CategoryModel.query.get(id)


def get_category_count() -> int:
    return CategoryModel.query.count()


def get_categories(params: Dict) -> List[object]:
    """Returns list of list of category model and count of total items"""
    categories = CategoryModel.query.paginate(
        params["page"], params["items_per_page"], False
    )

    return [categories.items, categories.total]


def create_category(data: Dict, user_id: int) -> CategoryModel:
    category = CategoryModel(name=data["name"], user_id=user_id)

    db.session.add(category)
    db.session.commit()

    return category


def update_category(data: Dict, category: CategoryModel) -> CategoryModel:
    category.name = data["name"]

    db.session.commit()

    return category


def delete_category(category: CategoryModel):
    db.session.delete(category)
    db.session.commit()
