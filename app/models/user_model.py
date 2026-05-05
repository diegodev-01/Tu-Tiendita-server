from enum import Enum
from pydantic import BaseModel
from typing import List, Optional
from app.models.permission_model import Permission


class Role(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    CUSTOMER = "customer"


class User(BaseModel):
    username: str
    roles: List[Role]
    permissions: List[Permission]


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    roles: List[Role]


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
