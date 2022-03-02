from datetime import datetime
from sqlalchemy_utils import EmailType

from main import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(EmailType, index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(12), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    def __str__(self) -> str:
        return f"<UserModel {self.id} {self.email}>"
