import uuid

from sqlalchemy.orm import Session

from app.models.transaction import Transaction, TransactionStatus


def create_transaction(
    db: Session,
    order_id: uuid.UUID,
    amount: float,
    transaction_ref: str,
    status: TransactionStatus,
) -> Transaction:
    db_transaction = Transaction(
        order_id=order_id,
        amount=amount,
        transaction_ref=transaction_ref,
        status=status,
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_all_transactions(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Transaction).offset(skip).limit(limit).all()
