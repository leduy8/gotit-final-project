from flask import jsonify, request

from main import app
from main.schemas.user import UserSchema
from main.commons.exceptions import BadRequest
from main.commons.decorators import validate_request
from main.engines import user as user_engine
from main.libs.jwt import create_access_token


@app.post('/users')
@validate_request('body', UserSchema)
def register_user():
    data = request.get_json()

    if user_engine.find_user_by_email(data['email']):
        raise BadRequest(error_data=data, error_message=f'Email is already registered.')

    user = user_engine.create_user(data)

    return jsonify({'access_token': create_access_token({'id': user.id})}), 201
