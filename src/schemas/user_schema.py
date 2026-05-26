from typing import List, Optional
from pydantic import BaseModel, Field
from src.models.permission import Permission
from src.constants.PyObjectId import PyObjectId
from src.models.role import Role


class UserResponse(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    email: str
    roles: List[Role]
    permissions: List[Permission]

from datetime import datetime

class UserProfileResponse(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    email: str
    createdAt: datetime
