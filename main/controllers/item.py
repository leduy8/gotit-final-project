import random
from flask import jsonify, request
from marshmallow import ValidationError

from main import app
from main.commons.decorators import jwt_required, jwt_not_required
from main.schemas.item import ItemSchema
from main.schemas.base import PaginationSchema
from main.schemas.id import IdSchema
from main.engines.item import get_all, get_by_id, get_count, create, update, delete
from main.commons.exceptions import BadRequest, Forbidden, NotFound


@app.post('/items')
@jwt_required
def create_item(user_id):
    schema = ItemSchema()

    try:
        schema.load(data)
    except ValidationError as e:
        value = random.choice(list(e.messages.values()))
        raise BadRequest(error_data=e.data, error_message=value[0])

    data = request.get_json() or {}
    item = create(data, user_id)

    return jsonify(schema.dump(item)), 201


@app.get('/items')
@jwt_not_required
def get_items(user_id):
    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get(
        'items_per_page',
        app.config['ITEMS_PER_PAGE'],
        type=int
    )
    total_items = get_count()
    schema = PaginationSchema()

    try:
        schema.load({
            'page': page,
            'items_per_page': items_per_page,
            'total_items': total_items
        })
    except ValidationError as e:
        value = random.choice(list(e.messages.values()))
        raise BadRequest(error_data=e.data, error_message=value[0])

    items = get_all({'page': page, 'items_per_page': items_per_page}, user_id)

    return jsonify({
        'items': items,
        'page': page,
        'items_per_page': items_per_page,
        'total_items': total_items
    })


@app.get('/items/<id>')
@jwt_not_required
def get_item_by_id(user_id, id):
    schema = IdSchema()

    try:
        schema.load({'id': id})
    except ValidationError as e:
        value = random.choice(list(e.messages.values()))
        raise BadRequest(error_data=e.data, error_message=value[0])

    item = get_by_id(id, user_id)

    if not item:
        raise NotFound(error_message=f'Item not found.')

    return jsonify(item)


@app.put('/items/<id>')
@jwt_required
def update_item_by_id(user_id, id):
    item = get_by_id(id, user_id)

    if not item:
        raise NotFound(error_message=f'Item not found.')

    if not item['is_owner']:
        raise Forbidden(error_message=f'Token is invalid or has been revoked.')

    data = request.get_json()
    item_schema = ItemSchema()
    id_schema = IdSchema()

    try:
        item_schema.load(data)
        id_schema.load({'id': id})
    except ValidationError as e:
        value = random.choice(list(e.messages.values()))
        raise BadRequest(error_data=e.data, error_message=value[0])

    updated_item = update(data, id)

    return jsonify(item_schema.dump(updated_item))


@app.delete('/items/<id>')
@jwt_required
def delete_item_by_id(user_id, id):
    schema = IdSchema()

    try:
        schema.load({'id': id})
    except ValidationError as e:
        value = random.choice(list(e.messages.values()))
        raise BadRequest(error_data=e.data, error_message=value[0])

    item = get_by_id(id, user_id)

    if not item:
        raise NotFound(error_message='Item not found.')

    if not item['is_owner']:
        raise Forbidden(error_message='Token is invalid or has been revoked.')

    delete(id)

    return jsonify({})
