import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate


def get_category_by_id(db: Session, category_id: uuid.UUID) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()


def get_all_categories(db: Session):
    return db.query(Category).all()


def create_category(db: Session, category_in: CategoryCreate) -> Category:
    db_category = Category(**category_in.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
