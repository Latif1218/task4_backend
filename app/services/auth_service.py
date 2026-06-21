from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.crud.crud_user import create_user, get_user_by_email
from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate


def register_user(db: Session, user_in: UserCreate):
    existing_user = get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="এই Email দিয়ে আগেই একটা Account তৈরি করা হয়েছে",
        )
    user = create_user(db, user_in)
    return user


def authenticate_user(db: Session, login_in: LoginRequest):
    user = get_user_by_email(db, login_in.email)
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email বা Password ভুল হয়েছে",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="আপনার Account নিষ্ক্রিয় (Inactive) করে রাখা হয়েছে",
        )

    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )
    return access_token, user
