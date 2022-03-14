from tests.data_mocker import create_dummy_email


def test_success_login_user(client, user):
    response = client.post(
        "/auth",
        json={"email": "duy123@gmail.com", "password": "123456"},
        content_type="application/json",
    )

    assert response.status_code == 200
    assert type(response.data) == bytes
    assert len(response.data.decode("utf-8").split(".")) == 3


def test_fail_login_user_with_wrong_email_format(client, user):
    response = client.post(
        "/auth",
        json={"email": "duy123gmail.com", "password": "123456"},
        content_type="application/json",
    )

    assert response.status_code == 400


def test_fail_login_user_with_missing_email(client, user):
    response = client.post(
        "/auth", json={"password": "123456"}, content_type="application/json"
    )

    assert response.status_code == 400


def test_fail_login_user_with_missing_passsword(client, user):
    response = client.post(
        "/auth", json={"email": "duy123@gmail.com"}, content_type="application/json"
    )

    assert response.status_code == 400


def test_fail_login_user_with_invalid_email_length(client, user):
    response = client.post(
        "/auth",
        json={"email": create_dummy_email(), "password": "123456"},
        content_type="application/json",
    )

    assert response.status_code == 400


def test_fail_login_user_with_invalid_passsword_length(client, user):
    response = client.post(
        "/auth",
        json={"email": "duy123@gmail.com", "password": "12345"},
        content_type="application/json",
    )

    assert response.status_code == 400


def test_fail_login_user_with_wrong_email_or_password(client, user):
    response = client.post(
        "/auth",
        json={"email": "duy12345@gmail.com", "password": "123456"},
        content_type="application/json",
    )

    assert response.status_code == 401
