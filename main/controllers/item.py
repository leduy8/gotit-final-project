from flask import jsonify, request

from main import app
from main.commons.decorators import require_authorized_user, require_non_authoried_user, validate_request
from main.schemas.item import ItemSchema
from main.schemas.base import PaginationSchema
from main.engines import item as item_engine
from main.commons.exceptions import Forbidden, NotFound


@app.post('/items')
@require_authorized_user
@validate_request('body', ItemSchema)
def create_item(user_id):
    data = request.get_json() or {}
    item = item_engine.create_item(data, user_id)

    return ItemSchema().jsonify(item), 201


@app.get('/items')
@require_non_authoried_user
@validate_request('params', PaginationSchema)
def get_items(user_id):
    params = {
        'page': request.args.get('page', 1, type=int),
        'items_per_page': request.args.get('items_per_page', app.config['ITEMS_PER_PAGE'], type=int),
        'total_items': item_engine.get_item_count()
    }

    items = item_engine.get_all_items(params, user_id)

    return jsonify(items)


@app.get('/items/<int:id>')
@require_non_authoried_user
def get_item_by_id(user_id, id):
    item = item_engine.get_item_by_id(id, user_id)

    if not item:
        raise NotFound(error_message=f'Item not found.')

    return jsonify(item)


@app.put('/items/<int:id>')
@require_authorized_user
@validate_request('body', ItemSchema)
def update_item_by_id(user_id, id):
    item = item_engine.get_item_by_id(id, user_id)

    if not item:
        raise NotFound(error_message=f'Item not found.')

    if not item['is_owner']:
        raise Forbidden(error_message=f'Token is invalid or has been revoked.')

    data = request.get_json()
    updated_item = item_engine.update_item(data, id)

    return ItemSchema().jsonify(updated_item)


@app.delete('/items/<int:id>')
@require_authorized_user
def delete_item_by_id(user_id, id):
    item = item_engine.get_item_by_id(id, user_id)

    if not item:
        raise NotFound(error_message='Item not found.')

    if not item['is_owner']:
        raise Forbidden(error_message='Token is invalid or has been revoked.')

    item_engine.delete_item(id)

    return jsonify({})
