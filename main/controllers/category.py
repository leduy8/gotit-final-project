from flask import jsonify, request

from main import app
from main.commons.decorators import jwt_required, jwt_not_required, load_id_schema, load_schema
from main.commons.exceptions import BadRequest, NotFound, Forbidden
from main.engines.category import delete, find_by_name, create, get_all, get_count, get_by_id, update
from main.schemas.base import PaginationSchema
from main.schemas.category import CategorySchema


@app.post('/categories')
@jwt_required
@load_schema('body', CategorySchema)
def create_category(user_id):
    data = request.get_json() or {}

    if find_by_name(data['name']):
        raise BadRequest(
            error_message=f'Category with name={data["name"]} has already been used.')

    category = create(data, user_id)

    return jsonify(CategorySchema().dump(category)), 201


@app.get('/categories')
@jwt_not_required
@load_schema('params', PaginationSchema)
def get_categories(user_id):
    params = {
        'page': request.args.get('page', 1, type=int),
        'items_per_page': request.args.get('items_per_page', app.config['CATEGORIES_PER_PAGE'], type=int),
        'total_items': get_count()
    }

    categories = get_all(params, user_id)

    return jsonify(categories)


@app.get('/categories/<id>')
@jwt_not_required
@load_id_schema
def get_category_by_id(user_id, id):
    category = get_by_id(id, user_id)

    if not category:
        raise NotFound(error_message=f'Category not found.')

    return jsonify(category)


@app.put('/categories/<id>')
@jwt_required
@load_id_schema
@load_schema('body', CategorySchema)
def update_category_by_id(user_id, id):
    category = get_by_id(id, user_id)

    if not category:
        raise NotFound(error_message='Category not found.')

    if not category['is_owner']:
        raise Forbidden(error_message='Token is invalid or has been revoked.')

    data = request.get_json()
    updated_category = update(data, id)

    if not updated_category:
        raise BadRequest(
            error_message=f'Category with name={data["name"]} has already been used.'
        )

    return jsonify(CategorySchema().dump(updated_category))


@app.delete('/categories/<id>')
@jwt_required
@load_id_schema
def delete_category_by_id(user_id, id):
    category = get_by_id(id, user_id)

    if not category:
        raise NotFound(error_message='Category not found.')

    if not category['is_owner']:
        raise Forbidden(error_message='Token is invalid or has been revoked.')

    delete(id)

    return jsonify({})
