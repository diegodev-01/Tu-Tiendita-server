from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List, Optional

from models.transaction_item import TransactionItem
from models.transaction_status import TransactionStatus


class Transaction(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    storeId: str
    orderNumber: str = Field(pattern=r"^ORD-\d+$")
    provider: str
    status: TransactionStatus = TransactionStatus.PENDING
    estimatedArrival: Optional[datetime] = None
    item: List[TransactionItem]
    cratedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
