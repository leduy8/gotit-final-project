from flask import jsonify, request
from marshmallow import ValidationError

from main import app, db
from main.models.user import UserModel
from main.schemas.user import UserSchema
from main.commons.exceptions import BadRequest
from main.engines.user import find_by_email
from main.libs.password_utils import gen_salt, generate_password_hash
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

    salt = gen_salt()
    password_hash = generate_password_hash(data['password'], salt)

    user = UserModel(
        email=data['email'],
        password_hash=password_hash,
        salt=salt
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({'access_token': create_access_token({'id': user.id})}), 201
