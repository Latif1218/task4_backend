import uuid
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate


def get_service_by_id(db: Session, service_id: uuid.UUID) -> Optional[Service]:
    return db.query(Service).filter(Service.id == service_id).first()


def get_services(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    category_id: Optional[uuid.UUID] = None,
    vendor_id: Optional[uuid.UUID] = None,
    only_active: bool = True,
):
    query = db.query(Service)

    if only_active:
        query = query.filter(Service.is_active == True)  # noqa: E712

    if search:
        query = query.filter(
            or_(
                Service.title.ilike(f"%{search}%"),
                Service.description.ilike(f"%{search}%"),
            )
        )

    if category_id:
        query = query.filter(Service.category_id == category_id)

    if vendor_id:
        query = query.filter(Service.vendor_id == vendor_id)

    return query.offset(skip).limit(limit).all()


def create_service(db: Session, vendor_id: uuid.UUID, service_in: ServiceCreate) -> Service:
    db_service = Service(vendor_id=vendor_id, **service_in.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def update_service(db: Session, service: Service, service_in: ServiceUpdate) -> Service:
    for field, value in service_in.model_dump(exclude_unset=True).items():
        setattr(service, field, value)
    db.commit()
    db.refresh(service)
    return service


def delete_service(db: Session, service: Service) -> None:
    db.delete(service)
    db.commit()
