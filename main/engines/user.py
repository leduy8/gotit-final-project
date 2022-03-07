from main.models.user import UserModel
from main.libs.password_utils import check_password_hash


def find_by_email(email: str) -> UserModel:
    return UserModel.query.filter_by(email=email).first()


def find_by_id(id: int) -> UserModel:
    return UserModel.query.filter_by(id=id).first()


def find_by_email_and_password(email: str, password: str):
    user = UserModel.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password, user.salt):
        return None

    return user
