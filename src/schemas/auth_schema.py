from pydantic import BaseModel
from typing import List
from src.models.user import Role, Permission


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserAuthDetails(BaseModel):
    name: str
    email: str
    roles: List[Role]
    permissions: List[Permission]


class Token(BaseModel):
    access_token: str
    token_type: str
