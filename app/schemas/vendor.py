import uuid
from typing import Optional

from pydantic import BaseModel

from app.schemas.user import UserOut


class VendorBase(BaseModel):
    business_name: str
    description: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    business_name: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class VendorOut(VendorBase):
    id: uuid.UUID
    rating: float
    user: UserOut

    class Config:
        from_attributes = True
