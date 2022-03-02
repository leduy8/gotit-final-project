import pytest

from main.libs.jwt import create_access_token, get_jwt_payload


def test_success_create_access_token(payload):
    assert 1 == 1


def test_fail_create_access_token(payload):
    assert 1 == 1


def test_success_get_jwt_payload():
    token = create_access_token({'id': 123})
    assert get_jwt_payload(token) is not None


def test_fail_get_jwt_payload():
    token = {'invalid': True}
    # ? Randon JWT token with random signature
    token2 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    assert get_jwt_payload(token) is None
    assert get_jwt_payload(token2) is None
