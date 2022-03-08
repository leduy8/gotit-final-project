from tests.controllers.create_data import create_dummy_category, create_dummy_item, get_dummy_jwt


def test_success_create_item(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)

    response = client.post(
        '/items',
        json={
            'name': 'Item 1',
            'description': 'My description',
            'category_id': category_id
        },
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 201
    assert type(response.json) == dict


def test_fail_create_item_missing_name(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)

    response = client.post(
        '/items',
        json={
            'description': 'My description',
            'category_id': category_id
        },
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_create_item_missing_category_id(client):
    jwt = get_dummy_jwt(client)

    response = client.post(
        '/items',
        json={
            'name': 'Item 1',
            'description': 'My description',
        },
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_create_item_missing_token(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)

    response = client.post(
        '/items',
        json={
            'name': 'Item 1',
            'description': 'My description',
            'category_id': category_id
        },
        content_type='application/json',
    )

    assert response.status_code == 401


def test_fail_create_item_invalid_name(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    dummy_text = ['a' for _ in range(60)]

    response = client.post(
        '/items',
        json={
            'name': dummy_text,
            'description': 'My description',
            'category_id': category_id
        },
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_create_item_invalid_description(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    dummy_text = ['a' for _ in range(210)]

    response = client.post(
        '/items',
        json={
            'name': 'Item 1',
            'description': dummy_text,
            'category_id': category_id
        },
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_create_item_invalid_description(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)

    response = client.post(
        '/items',
        json={
            'name': 'Item 1',
            'description': 'My description',
            'category_id': category_id * -1
        },
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_create_item_invalid_token(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)

    response = client.post(
        '/items',
        json={
            'name': 'Item 1',
            'description': 'My description',
            'category_id': category_id,
        },
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}wrong'}
    )

    assert response.status_code == 403


# # * ====================================================================


def test_success_get_items(client):
    jwt = get_dummy_jwt(client)

    response = client.get(
        '/items?page=1&items_per_page=4',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 200


def test_fail_get_items_invalid_page(client):
    jwt = get_dummy_jwt(client)

    response = client.get(
        '/items?page=-1&items_per_page=4',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_get_items_invalid_items_per_page(client):
    jwt = get_dummy_jwt(client)

    response = client.get(
        '/items?page=1&items_per_page=-4',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


# * ====================================================================


def test_success_get_item_by_id(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)

    response = client.get(
        f'/items/{item_id}',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 200


def test_fail_get_item_by_id_invalid_id(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)

    response = client.get(
        f'/items/{item_id * -1}',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_get_item_by_id_invalid_id(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)

    response = client.get(
        f'/items/{item_id + 1000}',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 404


# * ====================================================================

def test_success_update_item_by_id(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)

    response = client.put(
        f'/items/{item_id}',
        content_type='application/json',
        json={
            'name': 'Item 1',
            'description': 'Funny',
            'category_id': category_id
        },
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 200


def test_fail_update_item_by_id_missing_name(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)

    response = client.put(
        f'/items/{item_id}',
        content_type='application/json',
        json={
            'description': 'Funny',
            'category_id': category_id
        },
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_update_item_by_id_missing_category_id(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)

    response = client.put(
        f'/items/{item_id}',
        content_type='application/json',
        json={
            'name': 'Item 1',
            'description': 'Funny',
        },
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_update_item_by_id_missing_token(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)

    response = client.put(
        f'/items/{item_id}',
        content_type='application/json',
        json={
            'name': 'Item 1',
            'description': 'Funny',
            'category_id': category_id
        },
    )

    assert response.status_code == 401


def test_fail_update_item_by_id_missing_token(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)

    response = client.put(
        f'/items/{item_id}',
        content_type='application/json',
        json={
            'name': 'Item 1',
            'description': 'Funny',
            'category_id': category_id
        },
        headers={'Authorization': f'Bearer {jwt}wrong'}
    )

    assert response.status_code == 403


def test_fail_update_item_by_id_invalid_name(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)
    dummy_text = ['a' for _ in range(60)]

    response = client.put(
        f'/items/{item_id}',
        content_type='application/json',
        json={
            'name': dummy_text,
            'description': 'Funny',
            'category_id': category_id
        },
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_update_item_by_id_invalid_description(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)
    dummy_text = ['a' for _ in range(210)]

    response = client.put(
        f'/items/{item_id}',
        content_type='application/json',
        json={
            'name': 'Item 1',
            'description': dummy_text,
            'category_id': category_id
        },
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_update_item_by_id_invalid_category_id(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)

    response = client.put(
        f'/items/{item_id}',
        content_type='application/json',
        json={
            'name': 'Item 1',
            'description': 'My description',
            'category_id': f'{category_id * -1}'
        },
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_update_item_by_id_not_found(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)

    response = client.put(
        f'/items/{item_id + 1000}',
        content_type='application/json',
        json={
            'name': 'Item 1',
            'description': 'My description',
            'category_id': f'{category_id}'
        },
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 404


# * ====================================================================


def test_success_delete_item_by_id(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)

    response = client.delete(
        f'/items/{item_id}',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 200


def test_fail_delete_item_by_id_missing_token(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)

    response = client.delete(
        f'/items/{item_id}',
    )

    assert response.status_code == 401


def test_fail_delete_item_by_id_invalid_token(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)

    response = client.delete(
        f'/items/{item_id}',
        headers={'Authorization': f'Bearer {jwt}wrong'}
    )

    assert response.status_code == 403


def test_fail_delete_item_by_id_not_found(client):
    jwt = get_dummy_jwt(client)
    category_id = create_dummy_category(client, jwt)
    item_id = create_dummy_item(client, jwt, category_id)

    response = client.delete(
        f'/items/{item_id + 1000}',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 404
