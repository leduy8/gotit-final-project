from typing import Dict

from main import db
from main.libs.password import gen_salt, generate_password_hash
from main.models.user import UserModel


def find_user_by_email(email: str) -> UserModel:
    return UserModel.query.filter_by(email=email).first()


def find_user_by_id(id: int) -> UserModel:
    return UserModel.query.filter_by(id=id).first()


def create_user(data: Dict) -> UserModel:
    salt = gen_salt()
    password_hash = generate_password_hash(data["password"], salt)

    user = UserModel(email=data["email"], password_hash=password_hash, salt=salt)

    db.session.add(user)
    db.session.commit()

    return user
