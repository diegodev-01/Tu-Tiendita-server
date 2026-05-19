from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class StoreCreate(BaseModel):
    name: str

class StoreUpdate(BaseModel):
    name: Optional[str] = None

class StoreResponse(BaseModel):
    id: str = Field(alias="_id")
    ownerId: str
    name: str
    createdAt: datetime
