from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from src.constants.PyObjectId import PyObjectId
from src.models.permission import Permission
from src.models.role import Role


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    roles: List[Role] = [Role.CUSTOMER]
    permissions: List[Permission] = Field(default=[Permission.PRODUCT_VIEW])
