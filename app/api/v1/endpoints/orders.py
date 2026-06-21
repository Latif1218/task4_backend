import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_roles
from app.crud.crud_order import (
    create_order,
    get_order_by_id,
    get_orders_by_user,
    get_orders_by_vendor_services,
    update_order_status,
)
from app.crud.crud_service import get_service_by_id, get_services
from app.crud.crud_vendor import get_vendor_by_user_id
from app.db.session import get_db
from app.models.order import OrderStatus
from app.models.user import User, UserRole
from app.schemas.order import OrderCreate, OrderOut, OrderUpdateStatus

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderOut, dependencies=[Depends(require_roles(UserRole.USER))])
def place_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """End-User একটা Service Book করবে (Payment আগে হয়নি, Order PENDING State-এ থাকবে)"""
    service = get_service_by_id(db, order_in.service_id)
    if not service or not service.is_active:
        raise HTTPException(status_code=404, detail="Service পাওয়া যায়নি বা Active নেই")

    total_amount = service.price * order_in.quantity
    return create_order(db, current_user.id, order_in, total_amount)


@router.get("/my-orders", response_model=List[OrderOut])
def my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """End-User-এর নিজের Order History"""
    return get_orders_by_user(db, current_user.id)


@router.get(
    "/vendor-orders",
    response_model=List[OrderOut],
    dependencies=[Depends(require_roles(UserRole.VENDOR))],
)
def vendor_received_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Vendor-এর Dashboard-এ আসা সব Order দেখানোর জন্য"""
    vendor = get_vendor_by_user_id(db, current_user.id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor Profile পাওয়া যায়নি")

    services = get_services(db, vendor_id=vendor.id, only_active=False, limit=1000)
    service_ids = [s.id for s in services]
    return get_orders_by_vendor_services(db, service_ids)


@router.put(
    "/{order_id}/status",
    response_model=OrderOut,
    dependencies=[Depends(require_roles(UserRole.VENDOR, UserRole.ADMIN))],
)
def change_order_status(
    order_id: uuid.UUID,
    status_in: OrderUpdateStatus,
    db: Session = Depends(get_db),
):
    """Vendor অর্ডার Confirm/Complete/Cancel করতে পারবে"""
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order পাওয়া যায়নি")
    return update_order_status(db, order, status_in.status)
