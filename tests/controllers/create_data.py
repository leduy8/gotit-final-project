def create_dummy_user(client):
    client.post(
        '/users',
        json={
            'email': 'duy123@gmail.com',
            'password': '123456'
        },
        content_type='application/json'
    )


def create_dummy_item():
    pass


def create_dummy_category():
    pass
