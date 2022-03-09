from flask import jsonify, request

from main import app
from main.commons.decorators import validate_request
from main.commons.exceptions import Unauthorized
from main.schemas.user import UserSchema
from main.engines import user as user_engine
from main.libs.jwt import create_access_token


@app.post('/auth')
@validate_request('body', UserSchema)
def login_user():
    data = request.get_json()
    user = user_engine.find_user_by_email_and_password(data['email'], data['password'])

    if not user:
        raise Unauthorized(error_data=data, error_message=f'Wrong email or password.')

    return jsonify({'access_token': create_access_token({'id': user.id})})
