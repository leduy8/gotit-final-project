from flask import jsonify, request
from marshmallow import ValidationError

from main import app
from main.commons.exceptions import BadRequest, Unauthorized
from main.schemas.user import UserSchema
from main.engines.user import find_by_email_and_password
from main.libs.jwt import create_access_token


@app.post('/auth')
def login_user():
    data = request.get_json()
    schema = UserSchema()

    try:
        schema.load(data)
    except ValidationError as e:
        raise BadRequest(error_data=e.data, error_message=e.messages)

    user = find_by_email_and_password(data['email'], data['password'])

    if not user:
        raise Unauthorized(error_data=data, error_message=f'Wrong email or password.')

    return jsonify({'access_token': create_access_token({'id': user.id})})