from pydantic import BaseModel
from typing import List
from src.models.permission import Permission
from src.models.role import Role


class User(BaseModel):
    username: str
    password: str
    roles: List[Role] = [Role.CUSTOMER]
    permissions: List[Permission] = [Permission.PRODUCT_VIEW]
