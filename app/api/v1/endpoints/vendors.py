from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_roles
from app.crud.crud_vendor import create_vendor, get_vendor_by_user_id, update_vendor
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.vendor import VendorCreate, VendorOut, VendorUpdate

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.post(
    "/profile",
    response_model=VendorOut,
    dependencies=[Depends(require_roles(UserRole.VENDOR))],
)
def setup_vendor_profile(
    vendor_in: VendorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = get_vendor_by_user_id(db, current_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="Vendor Profile আগেই তৈরি করা হয়েছে")
    return create_vendor(db, current_user.id, vendor_in)


@router.get(
    "/profile/me",
    response_model=VendorOut,
    dependencies=[Depends(require_roles(UserRole.VENDOR))],
)
def get_my_vendor_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vendor = get_vendor_by_user_id(db, current_user.id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor Profile পাওয়া যায়নি")
    return vendor


@router.put(
    "/profile/me",
    response_model=VendorOut,
    dependencies=[Depends(require_roles(UserRole.VENDOR))],
)
def update_my_vendor_profile(
    vendor_in: VendorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vendor = get_vendor_by_user_id(db, current_user.id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor Profile পাওয়া যায়নি")
    return update_vendor(db, vendor, vendor_in)
