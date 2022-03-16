from main import db
from main.models.base import BaseModel


class ItemModel(BaseModel):
    __tablename__ = "item"

    name = db.Column(db.String(80), index=True, nullable=False)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def __str__(self) -> str:
        return f"<Item {self.id} {self.name} {self.user_id} {self.category_id}>"
