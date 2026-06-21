from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.transaction import PaymentRequest, TransactionOut
from app.services.payment_service import process_mock_payment

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/checkout", response_model=TransactionOut)
def checkout_payment(
    payment_in: PaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Sandbox/Mock Payment Gateway।
    এখানে কোনো Real Payment Provider Call হয় না, পুরোটাই Simulate করা হয়েছে।
    Test Card Number শেষে '0000' দিলে Payment Fail হবে, অন্য কিছু দিলে Success হবে।
    """
    return process_mock_payment(db, current_user.id, payment_in)
