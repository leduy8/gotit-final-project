from typing import Dict, List

from flask import jsonify

from main import app
from main.commons.decorators import authorize_user, validate_request
from main.commons.exceptions import BadRequest, Forbidden, NotFound
from main.engines import category as category_engine
from main.models.category import CategoryModel
from main.schemas.base import PaginationSchema
from main.schemas.category import CategorySchema


def get_category_data(category: CategoryModel, user_id: int) -> Dict:
    return {
        "id": category.id,
        "name": category.name,
        "created": category.created,
        "updated": category.updated,
        "is_owner": category.user_id == user_id,
    }


def get_category_data_with_params_data(
    categories: List[CategoryModel], user_id, *args, **kwargs
):
    return {
        "categories": [get_category_data(category, user_id) for category in categories],
        "page": kwargs["params"]["page"],
        "items_per_page": kwargs["params"]["items_per_page"],
        "total_items": kwargs["params"]["total_items"],
    }


@app.post("/categories")
@authorize_user()
@validate_request(CategorySchema)
def create_category(data, user_id):
    if category_engine.find_category_by_name(data["name"]):
        raise BadRequest(error_message="Category name has already been used.")

    category = category_engine.create_category(data, user_id)

    return CategorySchema().jsonify(category)


@app.get("/categories")
@authorize_user(required=False)
@validate_request(PaginationSchema)
def get_categories(data, user_id):
    params = {
        "page": 1,
        "items_per_page": app.config["CATEGORIES_PER_PAGE"],
        "total_items": category_engine.get_category_count(),
    }

    if "page" in data:
        params["page"] = data["page"]

    if "items_per_page" in data:
        params["items_per_page"] = data["items_per_page"]

    categories = category_engine.get_categories(params)

    return jsonify(
        get_category_data_with_params_data(
            categories=categories, user_id=user_id, params=params
        )
    )


@app.get("/categories/<int:id>")
@authorize_user(required=False)
def get_category_by_id(user_id, id):
    category = category_engine.find_category_by_id(id)

    if not category:
        raise NotFound(error_message="Category not found.")

    return jsonify(get_category_data(category, user_id))


@app.put("/categories/<int:id>")
@authorize_user()
@validate_request(CategorySchema)
def update_category_by_id(data, user_id, id):
    category = category_engine.find_category_by_id(id)

    if not category:
        raise NotFound(error_message="Category not found.")

    if category.user_id != user_id:
        raise Forbidden(
            error_message="User doesn't have permission to update this category"
        )

    if category_engine.find_category_by_name(data["name"]):
        raise BadRequest(error_message="Category name has already been used.")

    updated_category = category_engine.update_category(data, id)

    return CategorySchema().jsonify(updated_category)


@app.delete("/categories/<int:id>")
@authorize_user()
def delete_category_by_id(user_id, id):
    category = category_engine.find_category_by_id(id)

    if not category:
        raise NotFound(error_message="Category not found.")

    if category.user_id != user_id:
        raise Forbidden(
            error_message="User doesn't have permission to delete this category"
        )

    category_engine.delete_category(id)

    return jsonify({})
