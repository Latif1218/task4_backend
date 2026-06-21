import enum
import uuid

from sqlalchemy import Column, String, ForeignKey, DateTime, Float, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class TransactionStatus(str, enum.Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), unique=True, nullable=False)

    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), default="sandbox_mock")
    transaction_ref = Column(String(100), unique=True, nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    order = relationship("Order", back_populates="transaction")
