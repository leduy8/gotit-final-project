from flask import jsonify, request
from marshmallow import ValidationError

from main import app
from main.commons.decorators import jwt_required, jwt_not_required
from main.commons.exceptions import BadRequest, NotFound, Forbidden
from main.engines.category import delete, find_by_name, create, get_all, get_count, get_by_id, update
from main.schemas.base import PaginationSchema
from main.schemas.category import CategorySchema
from main.schemas.id import IdSchema


@app.post('/categories')
@jwt_required
def create_category(user_id):
    data = request.get_json() or {}
    schema = CategorySchema()

    try:
        schema.load(data)
    except ValidationError as e:
        raise BadRequest(error_data=e.data, error_message=e.messages)

    if find_by_name(data['name']):
        raise BadRequest(
            error_message=f'Category with name={data["name"]} has already been used.')

    category = create(data, user_id)

    return jsonify(schema.dump(category)), 201


@app.get('/categories')
@jwt_not_required
def get_categories(user_id):
    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get(
        'items_per_page', app.config['CATEGORIES_PER_PAGE'], type=int)
    total_items = get_count()
    schema = PaginationSchema()

    try:
        schema.load({
            'page': page,
            'items_per_page': items_per_page,
            'total_items': total_items
        })
    except ValidationError as e:
        raise BadRequest(error_data=e.data, error_message=e.messages)

    categories = get_all({'page': page, 'items_per_page': items_per_page}, user_id)

    return jsonify({
        'categories': categories,
        'page': page,
        'items_per_page': items_per_page,
        'total_items': total_items,
    })


@app.get('/categories/<id>')
@jwt_not_required
def get_category_by_id(user_id, id):
    category = get_by_id(id, user_id)
    schema = IdSchema()

    try:
        schema.load({'id': id})
    except ValidationError as e:
        raise BadRequest(error_data=id, error_message=e.messages)

    if not category:
        raise NotFound(error_message=f'Category not found.')

    return jsonify(category)


@app.put('/categories/<id>')
@jwt_required
def update_category_by_id(user_id, id):
    category = get_by_id(id, user_id)

    if not category:
        raise NotFound(error_message='Category not found.')

    if not category['is_owner']:
        raise Forbidden(error_message='Token is invalid or has been revoked.')

    data = request.get_json()
    category_schema = CategorySchema()
    id_schema = IdSchema()

    try:
        category_schema.load(data)
        id_schema.load({'id': id})
    except ValidationError as e:
        raise BadRequest(error_data=e.data, error_message=e.messages)

    updated_category = update(data, id)

    if not updated_category:
        raise BadRequest(
            error_message=f'Category with name={data["name"]} has already been used.')

    return jsonify(category_schema.dump(updated_category))


@app.delete('/categories/<id>')
@jwt_required
def delete_category_by_id(user_id, id):
    category = get_by_id(id, user_id)
    schema = IdSchema()

    try:
        schema.load({'id': id})
    except ValidationError as e:
        raise BadRequest(error_data=id, error_message=e.messages)

    if not category:
        raise NotFound(error_message='Category not found.')

    if not category['is_owner']:
        raise Forbidden(error_message='Token is invalid or has been revoked.')

    delete(id)

    return jsonify({})
