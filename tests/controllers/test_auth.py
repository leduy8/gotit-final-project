from tests.controllers.create_data import create_dummy_user


def test_success_login_user(client):
    create_dummy_user(client)

    response = client.post(
        '/auth',
        json={
            'email': 'duy123@gmail.com',
            'password': '123456'
        },
        content_type='application/json'
    )

    assert response.status_code == 200
    assert type(response.data) == bytes
    assert len(response.data.decode('utf-8').split('.')) == 3


def test_fail_login_user_wrong_email_format(client):
    response = client.post(
        '/auth',
        json={
            'email': 'duy123gmail.com',
            'password': '123456'
        },
        content_type='application/json'
    )

    assert response.status_code == 400


def test_fail_login_user_missing_email(client):
    response = client.post(
        '/auth',
        json={
            'password': '123456'
        },
        content_type='application/json'
    )

    assert response.status_code == 400


def test_fail_login_user_missing_passsword(client):
    response = client.post(
        '/auth',
        json={
            'email': 'duy123@gmail.com'
        },
        content_type='application/json'
    )

    assert response.status_code == 400


def test_fail_login_user_invalid_email_length(client):
    dummy_text = ''.join('a' for _ in range(50)) + '@' + \
        ''.join('a' for _ in range(250))

    response = client.post(
        '/auth',
        json={
            'email': dummy_text,
            'password': '123456'
        },
        content_type='application/json'
    )

    assert response.status_code == 400


def test_fail_login_user_invalid_passsword_length(client):
    response = client.post(
        '/auth',
        json={
            'email': 'duy123@gmail.com',
            'password': '12345'
        },
        content_type='application/json'
    )

    assert response.status_code == 400


def test_fail_login_user_wrong_email_or_password(client):
    create_dummy_user(client)

    response = client.post(
        '/auth',
        json={
            'email': 'duy12345@gmail.com',
            'password': '123456'
        },
        content_type='application/json'
    )

    assert response.status_code == 401
