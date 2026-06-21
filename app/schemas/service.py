import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.category import CategoryOut


class ServiceBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None


class ServiceCreate(ServiceBase):
    category_id: uuid.UUID


class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    category_id: Optional[uuid.UUID] = None
    is_active: Optional[bool] = None


class ServiceOut(ServiceBase):
    id: uuid.UUID
    vendor_id: uuid.UUID
    is_active: bool
    category: CategoryOut
    created_at: datetime

    class Config:
        from_attributes = True
