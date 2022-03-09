from flask import jsonify, request

from main import app
from main.commons.decorators import require_authorized_user, require_non_authoried_user, validate_request
from main.commons.exceptions import BadRequest, NotFound, Forbidden
from main.engines import category as category_engine
from main.schemas.base import PaginationSchema
from main.schemas.category import CategorySchema


@app.post('/categories')
@require_authorized_user
@validate_request('body', CategorySchema)
def create_category(user_id):
    data = request.get_json() or {}

    if category_engine.find_category_by_name(data['name']):
        raise BadRequest(
            error_message=f'Category with name={data["name"]} has already been used.')

    category = category_engine.create_category(data, user_id)

    return CategorySchema().jsonify(category), 201


@app.get('/categories')
@require_non_authoried_user
@validate_request('params', PaginationSchema)
def get_categories(user_id):
    params = {
        'page': request.args.get('page', 1, type=int),
        'items_per_page': request.args.get('items_per_page', app.config['CATEGORIES_PER_PAGE'], type=int),
        'total_items': category_engine.get_category_count()
    }

    categories = category_engine.get_all_categories(params, user_id)

    return jsonify(categories)


@app.get('/categories/<id>')
@require_non_authoried_user
def get_category_by_id(user_id, id):
    category = category_engine.get_category_by_id(id, user_id)

    if not category:
        raise NotFound(error_message=f'Category not found.')

    return jsonify(category)


@app.put('/categories/<id>')
@require_authorized_user
@validate_request('body', CategorySchema)
def update_category_by_id(user_id, id):
    category = category_engine.get_category_by_id(id, user_id)

    if not category:
        raise NotFound(error_message='Category not found.')

    if not category['is_owner']:
        raise Forbidden(error_message='Token is invalid or has been revoked.')

    data = request.get_json()
    updated_category = category_engine.update_category(data, id)

    if not updated_category:
        raise BadRequest(
            error_message=f'Category with name={data["name"]} has already been used.'
        )

    return CategorySchema().jsonify(updated_category)


@app.delete('/categories/<id>')
@require_authorized_user
def delete_category_by_id(user_id, id):
    category = category_engine.get_category_by_id(id, user_id)

    if not category:
        raise NotFound(error_message='Category not found.')

    if not category['is_owner']:
        raise Forbidden(error_message='Token is invalid or has been revoked.')

    category_engine.delete_category(id)

    return jsonify({})
