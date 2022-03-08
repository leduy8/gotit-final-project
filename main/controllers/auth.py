from flask import jsonify, request

from main import app
from main.commons.decorators import load_schema
from main.commons.exceptions import Unauthorized
from main.schemas.user import UserSchema
from main.engines.user import find_by_email_and_password
from main.libs.jwt import create_access_token


@app.post('/auth')
@load_schema('body', UserSchema)
def login_user():
    data = request.get_json()
    user = find_by_email_and_password(data['email'], data['password'])

    if not user:
        raise Unauthorized(error_data=data, error_message=f'Wrong email or password.')

    return jsonify({'access_token': create_access_token({'id': user.id})})
