from flask import jsonify

from main import app
from main.commons.decorators import pass_data
from main.commons.exceptions import BadRequest
from main.engines import user as user_engine
from main.libs.jwt import create_access_token
from main.libs.password import gen_salt, generate_password_hash
from main.schemas.load.user import LoadUserSchema


@app.post("/users")
@pass_data(LoadUserSchema)
def register_user(data):
    if user_engine.find_user_by_email(data["email"]):
        raise BadRequest(error_message="Email is already registered")

    data["password_salt"] = gen_salt()
    data["password_hash"] = generate_password_hash(
        data["password"], data["password_salt"]
    )

    user = user_engine.create_user(data)

    return jsonify({"access_token": create_access_token({"id": user.id})})
