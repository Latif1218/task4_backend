import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate


def get_vendor_by_user_id(db: Session, user_id: uuid.UUID) -> Optional[Vendor]:
    return db.query(Vendor).filter(Vendor.user_id == user_id).first()


def get_vendor_by_id(db: Session, vendor_id: uuid.UUID) -> Optional[Vendor]:
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()


def create_vendor(db: Session, user_id: uuid.UUID, vendor_in: VendorCreate) -> Vendor:
    db_vendor = Vendor(user_id=user_id, **vendor_in.model_dump())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor


def update_vendor(db: Session, vendor: Vendor, vendor_in: VendorUpdate) -> Vendor:
    for field, value in vendor_in.model_dump(exclude_unset=True).items():
        setattr(vendor, field, value)
    db.commit()
    db.refresh(vendor)
    return vendor


def get_all_vendors(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Vendor).offset(skip).limit(limit).all()
