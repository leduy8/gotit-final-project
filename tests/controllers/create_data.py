def get_dummy_jwt(client):
    response = create_dummy_user(client)

    return response.json['access_token']


def create_dummy_user(client):
    response = client.post(
        '/users',
        json={
            'email': 'duy123@gmail.com',
            'password': '123456'
        },
        content_type='application/json'
    )

    return response


def create_dummy_item(client, jwt, category_id):
    response = client.post(
        '/items',
        json={
            'name': 'Item 0',
            'description': 'My item 0 description',
            'category_id': category_id
        },
        headers={'Authorization': f'Bearer {jwt}'},
        content_type='application/json'
    )
    print(response.json)
    return response.json['id']


def create_dummy_category(client, jwt):
    response = client.post(
        '/categories',
        json={
            'name': 'Not Essentials',
        },
        headers={'Authorization': f'Bearer {jwt}'},
        content_type='application/json'
    )
    return response.json['id']
