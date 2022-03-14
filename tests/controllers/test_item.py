from tests.controllers.data_mocker import (
    create_dummy_access_token,
    create_dummy_category,
    create_dummy_item,
    create_dummy_text,
    create_dummy_user,
)

user = create_dummy_user()
access_token = create_dummy_access_token(user)
category = create_dummy_category(user.id)
item = create_dummy_item(category_id=category.id, user_id=user.id)


def test_success_create_item(client):
    response = client.post(
        "/items",
        json={
            "name": "Item 1",
            "description": "My description",
            "category_id": category.id,
        },
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 201
    assert type(response.json) == dict


def test_success_create_item_missing_description(client):
    response = client.post(
        "/items",
        json={"name": "Item 1", "category_id": category.id},
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 201
    assert type(response.json) == dict


def test_fail_create_item_with_missing_name(client):
    response = client.post(
        "/items",
        json={"description": "My description", "category_id": category.id},
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_create_item_with_missing_category_id(client):
    response = client.post(
        "/items",
        json={
            "name": "Item 1",
            "description": "My description",
        },
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_create_item_with_missing_token(client):
    response = client.post(
        "/items",
        json={
            "name": "Item 1",
            "description": "My description",
            "category_id": category.id,
        },
        content_type="application/json",
    )

    assert response.status_code == 401


def test_fail_create_item_with_invalid_name(client):
    response = client.post(
        "/items",
        json={
            "name": create_dummy_text(),
            "description": "My description",
            "category_id": category.id,
        },
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_create_item_with_invalid_description(client):
    response = client.post(
        "/items",
        json={
            "name": "Item 1",
            "description": create_dummy_text(length=210),
            "category_id": category.id,
        },
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_create_item_with_invalid_category_id(client):
    response = client.post(
        "/items",
        json={
            "name": "Item 1",
            "description": "My description",
            "category_id": category.id * -1,
        },
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_create_item_with_invalid_token(client):
    response = client.post(
        "/items",
        json={
            "name": "Item 1",
            "description": "My description",
            "category_id": category.id,
        },
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}wrong"},
    )

    assert response.status_code == 403


# # * ====================================================================


def test_success_get_items(client):
    response = client.get(
        "/items?page=1&items_per_page=4",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200


def test_success_get_items_without_token(client):
    response = client.get(
        "/items?page=1&items_per_page=4",
    )

    assert response.status_code == 200


def test_success_get_items_without_page(client):
    response = client.get(
        "/items?items_per_page=4", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200


def test_success_get_items_without_items_per_page(client):
    response = client.get(
        "/items?page=1", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200


def test_fail_get_items_with_invalid_token(client):
    response = client.get(
        "/items?page=1&items_per_page=4",
        headers={"Authorization": f"Bearer {access_token}wrong"},
    )

    assert response.status_code == 401


def test_fail_get_items_invalid_page(client):
    response = client.get(
        "/items?page=-1&items_per_page=4",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_get_items_invalid_items_per_page(client):
    response = client.get(
        "/items?page=1&items_per_page=-4",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


# * ====================================================================


def test_success_get_item_by_id(client):
    response = client.get(
        f"/items/{item.id}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200


def test_success_get_item_by_id_without_token(client):
    response = client.get(
        f"/items/{item.id}",
    )

    assert response.status_code == 200


def test_fail_get_item_by_id_with_invalid_token(client):
    response = client.get(
        f"/items/{item.id}", headers={"Authorization": f"Bearer {access_token}wrong"}
    )

    assert response.status_code == 401


def test_fail_get_item_by_id_with_invalid_id(client):
    response = client.get(
        f"/items/{item.id * -1}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 400


def test_fail_get_item_by_id_with_nonexistent_id(client):
    response = client.get(
        f"/items/{item.id + 1000}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 404


# * ====================================================================


def test_success_update_item_by_id(client):
    response = client.put(
        f"/items/{item.id}",
        content_type="application/json",
        json={"name": "Item 1", "description": "Funny", "category_id": category.id},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200


def test_success_update_item_by_id_with_missing_description(client):
    response = client.put(
        f"/items/{item.id}",
        content_type="application/json",
        json={"name": "Item 1", "category_id": category.id},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200


def test_fail_update_item_by_id_with_missing_name(client):
    response = client.put(
        f"/items/{item.id}",
        content_type="application/json",
        json={"description": "Funny", "category_id": category.id},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_update_item_by_id_with_missing_category_id(client):
    response = client.put(
        f"/items/{item.id}",
        content_type="application/json",
        json={
            "name": "Item 1",
            "description": "Funny",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_update_item_by_id_with_missing_token(client):
    response = client.put(
        f"/items/{item.id}",
        content_type="application/json",
        json={"name": "Item 1", "description": "Funny", "category_id": category.id},
    )

    assert response.status_code == 401


def test_fail_update_item_by_id_with_invalid_token(client):
    response = client.put(
        f"/items/{item.id}",
        content_type="application/json",
        json={"name": "Item 1", "description": "Funny", "category_id": category.id},
        headers={"Authorization": f"Bearer {access_token}wrong"},
    )

    assert response.status_code == 403


def test_fail_update_item_by_id_with_invalid_name(client):
    response = client.put(
        f"/items/{item.id}",
        content_type="application/json",
        json={
            "name": create_dummy_text(),
            "description": "Funny",
            "category_id": category.id,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_update_item_by_id_with_invalid_description(client):
    response = client.put(
        f"/items/{item.id}",
        content_type="application/json",
        json={
            "name": "Item 1",
            "description": create_dummy_text(length=210),
            "category_id": category.id,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_update_item_by_id_with_invalid_category_id(client):
    response = client.put(
        f"/items/{item.id}",
        content_type="application/json",
        json={
            "name": "Item 1",
            "description": "My description",
            "category_id": f"{category.id * -1}",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_fail_update_item_by_id_with_nonexistent_category_id(client):
    response = client.put(
        f"/items/{item.id}",
        content_type="application/json",
        json={
            "name": "Item 1",
            "description": "My description",
            "category_id": f"{category.id + 1000}",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404


def test_fail_update_item_by_id_with_nonexistent_id(client):
    response = client.put(
        f"/items/{item.id + 1000}",
        content_type="application/json",
        json={
            "name": "Item 1",
            "description": "My description",
            "category_id": f"{category.id}",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404


# * ====================================================================


def test_success_delete_item_by_id(client):
    another_item = create_dummy_item(category_id=category.id, user_id=user.id)

    response = client.delete(
        f"/items/{another_item.id}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200


def test_fail_delete_item_by_id_with_missing_token(client):
    another_item = create_dummy_item(category_id=category.id, user_id=user.id)

    response = client.delete(
        f"/items/{another_item.id}",
    )

    assert response.status_code == 401


def test_fail_delete_item_by_id_with_invalid_token(client):
    another_item = create_dummy_item(category_id=category.id, user_id=user.id)

    response = client.delete(
        f"/items/{another_item.id}",
        headers={"Authorization": f"Bearer {access_token}wrong"},
    )

    assert response.status_code == 403


def test_fail_delete_item_by_with_nonexistent_id(client):
    another_item = create_dummy_item(category_id=category.id, user_id=user.id)

    response = client.delete(
        f"/items/{another_item.id + 1000}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404
