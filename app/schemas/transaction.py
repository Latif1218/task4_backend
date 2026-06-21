import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.transaction import TransactionStatus


class PaymentRequest(BaseModel):
    order_id: uuid.UUID
    card_number: str  # Sandbox-এ যেকোনো নাম্বার দিলেই চলবে
    card_holder_name: str
    expiry: str
    cvv: str


class TransactionOut(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID
    amount: float
    payment_method: str
    transaction_ref: str
    status: TransactionStatus
    created_at: datetime

    class Config:
        from_attributes = True
