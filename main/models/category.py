from datetime import datetime

from main import db


class CategoryModel(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    def __str__(self) -> str:
        return f'<CategoryModel {self.id} {self.name}>'