from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_roles
from app.crud.crud_order import get_all_orders
from app.crud.crud_service import get_services
from app.crud.crud_transaction import get_all_transactions
from app.crud.crud_user import get_all_users
from app.crud.crud_vendor import get_all_vendors
from app.db.session import get_db
from app.models.user import UserRole
from app.schemas.order import OrderOut
from app.schemas.service import ServiceOut
from app.schemas.transaction import TransactionOut
from app.schemas.user import UserOut
from app.schemas.vendor import VendorOut

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_roles(UserRole.ADMIN))],
)


@router.get("/users", response_model=List[UserOut])
def list_all_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return get_all_users(db, skip, limit)


@router.get("/vendors", response_model=List[VendorOut])
def list_all_vendors(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return get_all_vendors(db, skip, limit)


@router.get("/services", response_model=List[ServiceOut])
def list_all_services(db: Session = Depends(get_db)):
    return get_services(db, only_active=False, limit=1000)


@router.get("/orders", response_model=List[OrderOut])
def list_all_orders(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return get_all_orders(db, skip, limit)


@router.get("/transactions", response_model=List[TransactionOut])
def list_all_transactions(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return get_all_transactions(db, skip, limit)
