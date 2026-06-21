import uuid

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    slug: str


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
