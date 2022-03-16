from typing import Dict

from main import db
from main.models.user import UserModel


def find_user_by_email(email: str) -> UserModel:
    return UserModel.query.filter_by(email=email).first()


def find_user_by_id(id: int) -> UserModel:
    return UserModel.query.get(id)


def create_user(data: Dict) -> UserModel:
    user = UserModel(
        email=data["email"],
        password_hash=data["password_hash"],
        password_salt=data["password_salt"],
    )

    db.session.add(user)
    db.session.commit()

    return user
