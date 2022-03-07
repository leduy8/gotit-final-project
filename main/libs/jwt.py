from typing import Dict
import jwt
from flask import request

from main import config
from main.commons.exceptions import Unauthorized


def create_access_token(payload: Dict) -> str:
    if type(payload) == dict:
        return jwt.encode(payload=payload, key=config.SECRET_KEY, algorithm='HS256')

    return None


def get_jwt_token() -> str:
    auth_header = request.headers.get('Authorization', None)

    if not auth_header or not auth_header.startswith('Bearer ') or len(auth_header.split(' ')) != 2:
        return None

    return auth_header.split(' ')[1]


def get_jwt_payload(token: str) -> Dict:
    try:
        return jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])
    except jwt.DecodeError:
        return None
