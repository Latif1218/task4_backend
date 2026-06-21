import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.order import OrderStatus
from app.schemas.service import ServiceOut


class OrderCreate(BaseModel):
    service_id: uuid.UUID
    quantity: float = 1
    note: Optional[str] = None


class OrderUpdateStatus(BaseModel):
    status: OrderStatus


class OrderOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    service: ServiceOut
    quantity: float
    total_amount: float
    status: OrderStatus
    note: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
