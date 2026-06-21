import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_vendor, require_roles
from app.crud.crud_service import (
    create_service,
    delete_service,
    get_service_by_id,
    get_services,
    update_service,
)
from app.db.session import get_db
from app.models.user import UserRole
from app.models.vendor import Vendor
from app.schemas.service import ServiceCreate, ServiceOut, ServiceUpdate

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("/", response_model=List[ServiceOut])
def list_services(
    search: Optional[str] = None,
    category_id: Optional[uuid.UUID] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """Public Endpoint - সবাই Service Browse/Search করতে পারবে"""
    return get_services(db, skip=skip, limit=limit, search=search, category_id=category_id)


@router.get("/{service_id}", response_model=ServiceOut)
def get_service_details(service_id: uuid.UUID, db: Session = Depends(get_db)):
    service = get_service_by_id(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service পাওয়া যায়নি")
    return service


@router.post("/", response_model=ServiceOut)
def add_service(
    service_in: ServiceCreate,
    db: Session = Depends(get_db),
    vendor: Vendor = Depends(get_current_vendor),
):
    """Vendor-only: নতুন Service তৈরি"""
    return create_service(db, vendor.id, service_in)


@router.put("/{service_id}", response_model=ServiceOut)
def edit_service(
    service_id: uuid.UUID,
    service_in: ServiceUpdate,
    db: Session = Depends(get_db),
    vendor: Vendor = Depends(get_current_vendor),
):
    service = get_service_by_id(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service পাওয়া যায়নি")
    if str(service.vendor_id) != str(vendor.id):
        raise HTTPException(status_code=403, detail="এই Service আপনার নয়")
    return update_service(db, service, service_in)


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_service(
    service_id: uuid.UUID,
    db: Session = Depends(get_db),
    vendor: Vendor = Depends(get_current_vendor),
):
    service = get_service_by_id(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service পাওয়া যায়নি")
    if str(service.vendor_id) != str(vendor.id):
        raise HTTPException(status_code=403, detail="এই Service আপনার নয়")
    delete_service(db, service)


@router.get(
    "/vendor/my-services",
    response_model=List[ServiceOut],
    dependencies=[Depends(require_roles(UserRole.VENDOR))],
)
def get_my_services(
    db: Session = Depends(get_db),
    vendor: Vendor = Depends(get_current_vendor),
):
    """Vendor Dashboard-এ নিজের Service List দেখানোর জন্য"""
    return get_services(db, vendor_id=vendor.id, only_active=False, limit=1000)
