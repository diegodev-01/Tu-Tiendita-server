from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
from src.constants.PyObjectId import PyObjectId


class Product(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    storeId: str
    ownerId: str
    name: str
    sku: str
    nfcTagId: str
    price: float
    stock: int
    minStock: int
    shelf: str
    status: str
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
