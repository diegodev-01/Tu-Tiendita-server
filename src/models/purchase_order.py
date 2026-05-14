from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List, Optional
from models.order_item import OrderItem


class PurchaseOrder(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    storeId: str
    cashierId: str
    subtotal: float = Field(ge=0)
    tax: float = Field(ge=0)
    totalAmount: float = Field(ge=0)
    items: List[OrderItem]
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
