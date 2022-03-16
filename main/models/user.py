from main import db
from main.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"

    email = db.Column(db.String(254), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    password_salt = db.Column(db.String(12), nullable=False)
    categories = db.relationship(
        "CategoryModel", backref="owner", cascade="all,delete", lazy="dynamic"
    )
    items = db.relationship(
        "ItemModel", backref="owner", cascade="all,delete", lazy="dynamic"
    )

    def __str__(self) -> str:
        return f"<UserModel {self.id} {self.email}>"
