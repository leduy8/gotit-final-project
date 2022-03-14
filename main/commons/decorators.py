import functools

import jwt
from flask import request
from marshmallow import ValidationError

from main.commons.exceptions import BadRequest, Forbidden, Unauthorized
from main.engines.user import find_user_by_id
from main.libs.jwt import get_jwt_payload, get_jwt_token
from main.schemas.base import BaseSchema


def authorize_user(required=True):
    def decorated(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_jwt_token()
            except ValueError:
                if required:
                    raise Unauthorized(error_message="Token is required.")
                return f(None, *args, **kwargs)

            try:
                data = get_jwt_payload(token)
                user = find_user_by_id(data["id"])

                if not user:
                    raise Forbidden(
                        error_message="Token is invalid or has been revoked."
                    )

                return f(user.id, *args, **kwargs)
            except jwt.DecodeError:
                raise Forbidden(error_message="Token is invalid or has been revoked.")

        return wrapper

    return decorated


def validate_request(schema: BaseSchema):
    def decorated(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            data = None
            try:
                if request.method in ["POST", "PUT"]:
                    data = schema().load(request.get_json())
                elif request.method in ["GET"]:
                    data = schema().load(request.args.to_dict())
            except ValidationError as e:
                raise BadRequest(
                    error_data=e.messages, error_message="Bad input value(s)"
                )

            return f(data, *args, **kwargs)

        return wrapper

    return decorated
