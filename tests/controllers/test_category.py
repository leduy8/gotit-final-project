from tests.controllers.create_data import create_dummy_category, get_dummy_jwt


def test_success_create_category(client):
    jwt = get_dummy_jwt(client)

    response = client.post(
        '/categories',
        json={
            'name': 'Essentials'
        },
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 201
    assert type(response.json) == dict


def test_fail_create_category_existing_name(client):
    jwt = get_dummy_jwt(client)
    create_dummy_category(client, jwt)

    response = client.post(
        '/categories',
        json={
            'name': 'Not Essentials'
        },
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_create_category_missing_name(client):
    jwt = get_dummy_jwt(client)
    create_dummy_category(client, jwt)

    response = client.post(
        '/categories',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_create_category_invalid_name_length(client):
    jwt = get_dummy_jwt(client)
    create_dummy_category(client, jwt)
    dummy_text = ''.join('a' for _ in range(60))

    response = client.post(
        '/categories',
        json={
            'name': dummy_text
        },
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_create_category_missing_token(client):
    jwt = get_dummy_jwt(client)
    create_dummy_category(client, jwt)

    response = client.post(
        '/categories',
        json={
            'name': 'Essentials'
        },
        content_type='application/json'
    )

    assert response.status_code == 401


# # * ============================================================

def test_success_get_categories(client):
    jwt = get_dummy_jwt(client)
    create_dummy_category(client, jwt)

    response = client.get(
        '/categories?page=1&items_per_page=4',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 200


def test_fail_get_categories_invalid_page(client):
    jwt = get_dummy_jwt(client)
    create_dummy_category(client, jwt)

    response = client.get(
        '/categories?page=-1&items_per_page=4',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_get_categories_invalid_items_per_page(client):
    jwt = get_dummy_jwt(client)
    create_dummy_category(client, jwt)

    response = client.get(
        '/categories?page=1&items_per_page=-4',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400

# # * ============================================================


def test_success_get_category_by_id(client):
    jwt = get_dummy_jwt(client)
    id = create_dummy_category(client, jwt)

    response = client.get(
        f'/categories/{id}',
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 200


def test_fail_get_category_by_id_not_found_id(client):
    jwt = get_dummy_jwt(client)
    id = create_dummy_category(client, jwt)

    response = client.get(
        f'/categories/{id + 10}',
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 404


def test_fail_get_category_by_id_invalid_id(client):
    jwt = get_dummy_jwt(client)
    id = create_dummy_category(client, jwt)

    response = client.get(
        f'/categories/0',
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 404


# # * ============================================================


def test_success_update_category_by_id(client):
    jwt = get_dummy_jwt(client)
    id = create_dummy_category(client, jwt)

    response = client.put(
        f'/categories/{id}',
        json={
            'name': 'Another Category'
        },
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 200
    assert type(response.json) == dict


def test_fail_update_category_by_id_missing_name(client):
    jwt = get_dummy_jwt(client)
    id = create_dummy_category(client, jwt)

    response = client.put(
        f'/categories/{id}',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_update_category_by_id_exists_name(client):
    jwt = get_dummy_jwt(client)
    id = create_dummy_category(client, jwt)

    response = client.put(
        f'/categories/{id}',
        json={
            'name': 'Not Essentials'
        },
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_update_category_by_id_missing_token(client):
    jwt = get_dummy_jwt(client)
    id = create_dummy_category(client, jwt)

    response = client.put(
        f'/categories/{id}',
        json={
            'name': 'Another Category'
        },
        content_type='application/json',
    )

    assert response.status_code == 401


def test_fail_update_category_by_id_invalid_token(client):
    jwt = get_dummy_jwt(client)
    id = create_dummy_category(client, jwt)
    print(id)

    response = client.put(
        f'/categories/{id}',
        json={
            'name': 'Another Category'
        },
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}wrong'}
    )

    assert response.status_code == 403


def test_fail_update_category_by_id_invalid_name_length(client):
    jwt = get_dummy_jwt(client)
    id = create_dummy_category(client, jwt)
    dummy_text = ['a' for _ in range(60)]

    response = client.put(
        f'/categories/{id}',
        json={
            'name': dummy_text
        },
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 400


def test_fail_update_category_by_id_not_found(client):
    jwt = get_dummy_jwt(client)
    id = create_dummy_category(client, jwt)

    response = client.put(
        f'/categories/{id + 1000}',
        json={
            'name': 'Another Category'
        },
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 404


# # * ============================================================


def test_success_delete_category_by_id(client):
    jwt = get_dummy_jwt(client)
    id = create_dummy_category(client, jwt)

    response = client.delete(
        f'/categories/{id}',
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 200


def test_fail_delete_category_by_id_missing_token(client):
    jwt = get_dummy_jwt(client)
    id = create_dummy_category(client, jwt)

    response = client.delete(
        f'/categories/{id}',
        content_type='application/json',
    )

    assert response.status_code == 401


def test_fail_delete_category_by_id_invalid_token(client):
    jwt = get_dummy_jwt(client)
    id = create_dummy_category(client, jwt)

    response = client.delete(
        f'/categories/{id}',
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}wrong'}
    )

    assert response.status_code == 403


def test_fail_delete_category_by_id_not_found(client):
    jwt = get_dummy_jwt(client)
    id = create_dummy_category(client, jwt)

    response = client.delete(
        f'/categories/{id + 1000}',
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt}'}
    )

    assert response.status_code == 404
