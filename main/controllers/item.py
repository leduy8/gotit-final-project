from flask import jsonify, request

from main import app
from main.commons.decorators import jwt_required, jwt_not_required, load_schema, load_id_schema
from main.schemas.item import ItemSchema
from main.schemas.base import PaginationSchema
from main.engines.item import get_all, get_by_id, get_count, create, update, delete
from main.commons.exceptions import Forbidden, NotFound


@app.post('/items')
@jwt_required
@load_schema('body', ItemSchema)
def create_item(user_id):
    data = request.get_json() or {}
    item = create(data, user_id)

    return jsonify(ItemSchema().dump(item)), 201


@app.get('/items')
@jwt_not_required
@load_schema('params', PaginationSchema)
def get_items(user_id):
    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get(
        'items_per_page',
        app.config['ITEMS_PER_PAGE'],
        type=int
    )

    items = get_all(
        {'page': page, 'items_per_page': items_per_page, 'total_items': get_count()},
        user_id
    )

    return jsonify(items)


@app.get('/items/<id>')
@jwt_not_required
@load_id_schema
def get_item_by_id(user_id, id):
    item = get_by_id(id, user_id)

    if not item:
        raise NotFound(error_message=f'Item not found.')

    return jsonify(item)


@app.put('/items/<id>')
@jwt_required
@load_id_schema
@load_schema('body', ItemSchema)
def update_item_by_id(user_id, id):
    item = get_by_id(id, user_id)

    if not item:
        raise NotFound(error_message=f'Item not found.')

    if not item['is_owner']:
        raise Forbidden(error_message=f'Token is invalid or has been revoked.')

    data = request.get_json()
    updated_item = update(data, id)

    return jsonify(ItemSchema().dump(updated_item))


@app.delete('/items/<id>')
@jwt_required
@load_id_schema
def delete_item_by_id(user_id, id):
    item = get_by_id(id, user_id)

    if not item:
        raise NotFound(error_message='Item not found.')

    if not item['is_owner']:
        raise Forbidden(error_message='Token is invalid or has been revoked.')

    delete(id)

    return jsonify({})
