from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


class Store(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    ownerId: str
    name: str
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
