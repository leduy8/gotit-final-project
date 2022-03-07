from flask import jsonify, request
from marshmallow import ValidationError

from main import app
from main.schemas.user import UserSchema
from main.commons.exceptions import BadRequest
from main.engines.user import find_by_email, create
from main.libs.jwt import create_access_token


@app.post('/users')
def register_user():
    data = request.get_json()
    schema = UserSchema()

    try:
        schema.load(data)
    except ValidationError as e:
        raise BadRequest(error_data=e.data, error_message=e.messages)

    if find_by_email(data['email']):
        raise BadRequest(error_data=data, error_message=f'Email is already registered.')

    user = create(data)

    return jsonify({'access_token': create_access_token({'id': user.id})}), 201
