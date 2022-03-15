from main.engines.category import create_category
from main.engines.item import create_item
from main.engines.user import create_user
from main.libs.jwt import create_access_token


def create_dummy_email(local_part_length=50, domain_part_length=250):
    return (
        "".join("a" for _ in range(local_part_length))
        + "@"
        + "".join("a" for _ in range(domain_part_length))
    )


def create_dummy_text(length=60):
    return "".join("a" for _ in range(length))


def create_dummy_access_token(user):
    return create_access_token({"id": user.id})


def create_dummy_user(email="duy123@gmail.com"):
    data = {"email": email, "password": "123456"}

    user = create_user(data=data)

    return user


def create_dummy_item(category_id, user_id):
    data = {
        "name": "Item 0",
        "description": "Like no other",
        "category_id": category_id,
    }

    item = create_item(data=data, user_id=user_id)

    return item


def create_dummy_category(user_id, name="Not Essentials"):
    data = {"name": name}

    category = create_category(data=data, user_id=user_id)

    return category
