from enum import Enum
from pydantic import BaseModel
from typing import List
from app.models.permission_model import Permission


class Role(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    CUSTOMER = "customer"


class User(BaseModel):
    username: str
    roles: List[Role]
    permissions: List[Permission]
