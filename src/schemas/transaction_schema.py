from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class CartItem(BaseModel):
    productId: str
    name: str
    price: float
    quantity: int

class NFCItem(BaseModel):
    nfcTagId: str
    quantity: int

class TransactionCreate(BaseModel):
    storeId: Optional[str] = None
    items: List[NFCItem]
    paymentMethod: str = Field(..., description="'efectivo' or 'qr'")

class TransactionResponse(BaseModel):
    id: str = Field(alias="_id")
    storeId: str
    cashierId: str
    items: List[CartItem]
    paymentMethod: str
    totalAmount: float
    totalItems: int
    createdAt: datetime
