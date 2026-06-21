import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.models.order import Order, OrderStatus
from app.schemas.order import OrderCreate


def get_order_by_id(db: Session, order_id: uuid.UUID) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders_by_user(db: Session, user_id: uuid.UUID):
    return db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()


def get_orders_by_vendor_services(db: Session, vendor_service_ids: list):
    return (
        db.query(Order)
        .filter(Order.service_id.in_(vendor_service_ids))
        .order_by(Order.created_at.desc())
        .all()
    )


def get_all_orders(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Order).offset(skip).limit(limit).all()


def create_order(db: Session, user_id: uuid.UUID, order_in: OrderCreate, total_amount: float) -> Order:
    db_order = Order(
        user_id=user_id,
        service_id=order_in.service_id,
        quantity=order_in.quantity,
        note=order_in.note,
        total_amount=total_amount,
        status=OrderStatus.PENDING,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order_status(db: Session, order: Order, status: OrderStatus) -> Order:
    order.status = status
    db.commit()
    db.refresh(order)
    return order
