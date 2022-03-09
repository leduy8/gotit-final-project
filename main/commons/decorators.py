import random
import functools
from typing_extensions import Literal
from marshmallow import ValidationError
from flask import request

from main.commons.exceptions import BadRequest, Forbidden, Unauthorized
from main.schemas.base import BaseSchema
from main.libs.jwt import get_jwt_token, get_jwt_payload
from main.engines.user import find_user_by_id


def require_authorized_user(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = get_jwt_token()

        if not token:
            raise Unauthorized(error_message='Token is required.')

        data = get_jwt_payload(token)
        user = find_user_by_id(data['id']) if data else None
        if not user:
            raise Forbidden(error_message='Token is invalid or has been revoked.')
        return f(user.id, *args, **kwargs)

    return decorated


def require_non_authoried_user(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = get_jwt_token()

        if not token:
            return f(None, *args, **kwargs)

        data = get_jwt_payload(token)
        user = find_user_by_id(data['id'])
        if not user:
            raise
        return f(user.id, *args, **kwargs)

    return decorated


def validate_request(data_source: Literal['body', 'params'], schema: BaseSchema):
    def decorated(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                if data_source == 'body':
                    schema().load(request.get_json())
                elif data_source == 'params':
                    schema().load(request.args.to_dict())
            except ValidationError as e:
                value = random.choice(list(e.messages.values()))
                raise BadRequest(error_data=e.data, error_message=value[0])

            return f(*args, **kwargs)

        return wrapper

    return decorated
