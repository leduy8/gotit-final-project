from tests.data_mocker import (
    create_dummy_access_token,
    create_dummy_text,
    create_dummy_user,
)


def test_success_create_category(client, access_token):
    response = client.post(
        "/categories",
        json={"name": "Essentials"},
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert type(response.json) == dict


def test_fail_create_category_with_existing_name(client, access_token, category):
    response = client.post(
        "/categories",
        json={"name": "Not Essentials"},
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_create_category_with_missing_name(client, access_token):
    response = client.post(
        "/categories", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 400


def test_fail_create_category_with_invalid_name_length(client, access_token):
    response = client.post(
        "/categories",
        json={"name": create_dummy_text()},
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_create_category_with_missing_token(client):
    response = client.post(
        "/categories", json={"name": "Essentials"}, content_type="application/json"
    )

    assert response.status_code == 401


def test_success_get_categories(client, access_token):
    response = client.get(
        "/categories?page=1&items_per_page=4",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200


def test_success_get_categories_without_token(client):
    response = client.get(
        "/categories?page=1&items_per_page=4",
    )

    assert response.status_code == 200


def test_success_get_categories_without_page(client, access_token):
    response = client.get(
        "/categories?items_per_page=4",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200


def test_success_get_categories_without_items_per_page(client, access_token):
    response = client.get(
        "/categories?page=1", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200


def test_fail_get_categories_with_invalid_token(client, access_token):
    response = client.get(
        "/categories?page=1&items_per_page=4",
        headers={"Authorization": f"Bearer {access_token}wrong"},
    )

    assert response.status_code == 403


def test_fail_get_categories_with_invalid_page(client, access_token):
    response = client.get(
        "/categories?page=-1&items_per_page=4",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_get_categories_with_invalid_items_per_page(client, access_token):
    response = client.get(
        "/categories?page=1&items_per_page=-4",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_success_get_category_by_id(client, access_token, category):
    response = client.get(
        f"/categories/{category.id}",
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200


def test_fail_get_category_by_id_with_nonexistent_id(client, access_token, category):
    response = client.get(
        f"/categories/{category.id + 1000}",
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404


def test_fail_get_category_by_id_with_invalid_id(client, access_token, category):
    response = client.get(
        f"/categories/{category.id * -1}",
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404


def test_success_update_category_by_id(client, access_token, category):
    response = client.put(
        f"/categories/{category.id}",
        json={"name": "Another Category"},
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert type(response.json) == dict


def test_fail_update_category_by_id_with_missing_name(client, access_token, category):
    response = client.put(
        f"/categories/{category.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_update_category_by_id_with_existing_name(client, access_token, category):
    response = client.put(
        f"/categories/{category.id}",
        json={"name": "Not Essentials"},
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_update_category_by_id_without_permission(client, category):
    user = create_dummy_user(email="something@gmail.com")
    access_token = create_dummy_access_token(user)

    response = client.put(
        f"/categories/{category.id}",
        json={"name": "Not Essentials"},
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 403


def test_fail_update_category_by_id_with_missing_token(client, category):
    response = client.put(
        f"/categories/{category.id}",
        json={"name": "Another Category"},
        content_type="application/json",
    )

    assert response.status_code == 401


def test_fail_update_category_by_id_with_invalid_token(client, access_token, category):
    response = client.put(
        f"/categories/{category.id}",
        json={"name": "Another Category"},
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}wrong"},
    )

    assert response.status_code == 403


def test_fail_update_category_by_id_with_invalid_name_length(
    client, access_token, category
):
    response = client.put(
        f"/categories/{category.id}",
        json={"name": create_dummy_text()},
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_update_category_by_with_invalid_id(client, access_token, category):
    response = client.put(
        f"/categories/{category.id * -1}",
        json={"name": "Another Category"},
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404


def test_fail_update_category_by_with_nonexistent_id(client, access_token, category):
    response = client.put(
        f"/categories/{category.id + 1000}",
        json={"name": "Another Category"},
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404


def test_success_delete_category_by_id(client, access_token, category):
    response = client.delete(
        f"/categories/{category.id}",
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200


def test_fail_delete_category_by_id_with_missing_token(client, access_token, category):
    response = client.delete(
        f"/categories/{category.id}",
        content_type="application/json",
    )

    assert response.status_code == 401


def test_fail_delete_category_by_id_with_invalid_token(client, access_token, category):
    response = client.delete(
        f"/categories/{category.id}",
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}wrong"},
    )

    assert response.status_code == 403


def test_fail_delete_category_by_with_nonexistent_id(client, access_token, category):
    response = client.delete(
        f"/categories/{category.id + 1000}",
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404
