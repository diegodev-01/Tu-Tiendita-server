from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Product(BaseModel):
    name: str
    price: float
    nfc_tag_id: str
    sync_date: datetime = Field(default_factory=datetime.utcnow)
    owner_id: Optional[str] = None
    is_active: bool = True
