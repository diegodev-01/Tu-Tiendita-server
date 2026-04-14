from pydantic import BaseModel, Field
from datetime import datetime

class ProductModel(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=1)
    nfc_tag_id: str = Field(..., min_length=1)
    sync_date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "name": "Coca Cola",
                "price": 10.5,
                "nfc_tag_id": "ABC123XYZ",
                "sync_date": "2026-04-14T12:00:00"
            }
        }