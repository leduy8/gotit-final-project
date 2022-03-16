import functools

import jwt
from flask import request
from marshmallow import ValidationError

from main.commons.exceptions import (
    BadRequest,
    InvalidAuthorizationError,
    MissingAuthorzationError,
    Unauthorized,
)
from main.engines.user import find_user_by_id
from main.libs.jwt import get_jwt_payload, get_jwt_token
from main.schemas.base import BaseSchema


def authenticate_user(required=True):
    def decorated(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_jwt_token()
            except (MissingAuthorzationError, InvalidAuthorizationError):
                if required:
                    raise Unauthorized(
                        error_message="Token is either missing or invalid"
                    )
                return f(None, *args, **kwargs)

            try:
                data = get_jwt_payload(token)
                user = find_user_by_id(data["id"])

                if not user:
                    raise Unauthorized(error_message="Token is invalid")

                return f(user.id, *args, **kwargs)
            except jwt.DecodeError:
                raise Unauthorized(error_message="Token is invalid")

        return wrapper

    return decorated


def pass_data(schema: BaseSchema):
    def decorated(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            data = None
            try:
                if request.method in ["GET", "DELETE"]:
                    data = schema().load(request.args.to_dict())
                else:
                    data = schema().load(request.get_json())
            except ValidationError as e:
                raise BadRequest(
                    error_data=e.messages, error_message="Invalid input value(s)"
                )

            return f(data, *args, **kwargs)

        return wrapper

    return decorated
