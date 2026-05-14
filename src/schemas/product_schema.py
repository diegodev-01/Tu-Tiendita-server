from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from src.constants.PyObjectId import PyObjectId


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)
    nfc_tag_id: str = Field(..., min_length=1)


class ProductCreate(BaseModel):
    storeId: Optional[str] = None
    name: str
    sku: str
    nfcTagId: Optional[str] = Field(default="No vinculado")
    price: Optional[float] = Field(default=0.0)
    stock: Optional[int] = Field(default=0)
    minStock: Optional[int] = Field(default=0)
    shelf: Optional[str] = Field(default="Sin asignar")
    status: Optional[str] = Field(default="inactivo")


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, gt=1)
    sku: Optional[str] = None
    nfcTagId: Optional[str] = Field(None, min_length=1)
    stock: Optional[int] = None
    minStock: Optional[int] = None
    shelf: Optional[str] = None
    status: Optional[str] = None


class ProductResponse(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    storeId: str
    name: str
    sku: str
    nfcTagId: str
    price: float
    stock: int
    minStock: int
    shelf: str
    status: str
    createdAt: datetime = Field(alias="createdAt")
    updatedAt: datetime = Field(alias="updatedAt")
