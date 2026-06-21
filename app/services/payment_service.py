import random
import string
import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.crud_order import get_order_by_id, update_order_status
from app.crud.crud_transaction import create_transaction
from app.models.order import OrderStatus
from app.models.transaction import TransactionStatus
from app.schemas.transaction import PaymentRequest


def generate_transaction_ref() -> str:
    return "TXN-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


def process_mock_payment(db: Session, user_id: uuid.UUID, payment_in: PaymentRequest):
    """
    এটা একটা Sandbox/Mock Payment Gateway।
    আসল Payment Provider-এর সাথে কোনো সংযোগ নেই, শুধু Simulate করা হচ্ছে।
    """
    order = get_order_by_id(db, payment_in.order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order পাওয়া যায়নি")

    if str(order.user_id) != str(user_id):
        raise HTTPException(status_code=403, detail="এই Order আপনার নয়")

    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=400, detail="এই Order-এর Payment আগেই সম্পন্ন হয়েছে বা বাতিল করা হয়েছে"
        )

    # --- Mock Validation Logic ---
    # Sandbox-এ Card Number শেষ হয় '0000' দিয়ে হলে Payment Fail হবে (টেস্ট করার জন্য)
    transaction_ref = generate_transaction_ref()

    if payment_in.card_number.strip().endswith("0000"):
        transaction = create_transaction(
            db,
            order_id=order.id,
            amount=order.total_amount,
            transaction_ref=transaction_ref,
            status=TransactionStatus.FAILED,
        )
        raise HTTPException(
            status_code=402,
            detail="Sandbox Payment Failed (Test Card ব্যবহার করা হয়েছে)",
        )

    # Payment Success ধরে নেওয়া হচ্ছে
    transaction = create_transaction(
        db,
        order_id=order.id,
        amount=order.total_amount,
        transaction_ref=transaction_ref,
        status=TransactionStatus.SUCCESS,
    )

    update_order_status(db, order, OrderStatus.PAID)

    return transaction
