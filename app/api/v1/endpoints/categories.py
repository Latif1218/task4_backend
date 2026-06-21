from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_roles
from app.crud.crud_category import create_category, get_all_categories
from app.db.session import get_db
from app.models.user import UserRole
from app.schemas.category import CategoryCreate, CategoryOut

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return get_all_categories(db)


@router.post(
    "/",
    response_model=CategoryOut,
    dependencies=[Depends(require_roles(UserRole.ADMIN))],
)
def add_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category_in)
