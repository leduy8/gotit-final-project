import logging
import functools
from main.commons.exceptions import Unauthorized
from main.libs.jwt import get_jwt_token, get_jwt_payload
from main.engines.user import find_by_id


def jwt_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = get_jwt_token()

        if not token:
            raise Unauthorized(error_message='Token is required.')

        try:
            data = get_jwt_payload(token)
            user = find_by_id(data['id'])
            if not user:
                raise
            return f(user.id, *args, **kwargs)
        except Exception as e:
            logging.exception(e)
            raise Unauthorized(error_message='Token is invalid or has been revoked.')

    return decorated


def jwt_not_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = get_jwt_token()

        if not token:
            return f(None, *args, **kwargs)

        try:
            data = get_jwt_payload(token)
            user = find_by_id(data['id'])
            if not user:
                raise
            return f(user.id, *args, **kwargs)
        except Exception as e:
            logging.exception(e)
            raise Unauthorized(error_message='Token is invalid or has been revoked.')

    return decorated
