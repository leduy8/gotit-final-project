from typing import Dict

import jwt
from flask import request

from main import config


def create_access_token(payload: Dict) -> str:
    if type(payload) == dict:
        return jwt.encode(payload=payload, key=config.SECRET_KEY, algorithm="HS256")

    raise TypeError("Payload must be a dictionary.")


def get_jwt_token() -> str:
    auth_header = request.headers.get("Authorization", None)

    if not auth_header:
        raise ValueError("Authorization header not found.")

    auth_header_split = auth_header.split(" ")

    if not auth_header.startswith("Bearer ") or len(auth_header_split) != 2:
        raise ValueError("Authorization header should be a valid jwt token.")

    return auth_header_split[1]


def get_jwt_payload(token: str) -> Dict:
    try:
        return jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
    except jwt.DecodeError as e:
        raise e
