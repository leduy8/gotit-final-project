from flask import jsonify

from main import app
from main.commons.decorators import validate_request
from main.commons.exceptions import BadRequest
from main.engines import user as user_engine
from main.libs.jwt import create_access_token
from main.schemas.user import UserSchema


@app.post("/users")
@validate_request(UserSchema)
def register_user(data):
    if user_engine.find_user_by_email(data["email"]):
        raise BadRequest(error_message="Email is already registered.")

    user = user_engine.create_user(data)

    return jsonify({"access_token": create_access_token({"id": user.id})})
