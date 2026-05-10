from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=1)
    nfc_tag_id: str = Field(..., min_length=1)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, gt=0)
    nfc_tag_id: Optional[str] = Field(None, min_length=1)


class ProductResponse(ProductBase):
    id: str
    sync_date: datetime

    class Config:
        from_attributes = True
