from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.crud.crud_user import get_user_by_id
from app.crud.crud_vendor import get_vendor_by_user_id
from app.db.session import get_db
from app.models.user import User, UserRole

# HTTPBearer ব্যবহার করা হয়েছে যাতে Swagger-এর "Authorize" Button-এ
# সরাসরি Token Paste করা যায় (Username/Password Form-Data লাগে না)
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token Verify করা যায়নি, আবার Login করুন",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = get_user_by_id(db, user_id)
    if user is None or not user.is_active:
        raise credentials_exception

    return user


def require_roles(*allowed_roles: UserRole):
    """
    Role-Based Access Control Dependency.
    Usage: Depends(require_roles(UserRole.ADMIN, UserRole.VENDOR))
    """

    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="এই Resource Access করার Permission আপনার নেই",
            )
        return current_user

    return role_checker


def get_current_vendor(
    current_user: User = Depends(require_roles(UserRole.VENDOR)),
    db: Session = Depends(get_db),
):
    """Vendor Role-এর User-এর Vendor Profile রিটার্ন করে"""
    vendor = get_vendor_by_user_id(db, current_user.id)
    if vendor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor Profile পাওয়া যায়নি, আগে Profile Setup করুন",
        )
    return vendor