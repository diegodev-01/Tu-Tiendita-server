from pydantic import BaseModel
from typing import List
from src.models.user import Role, Permission


class UserCreate(BaseModel):
    username: str
    password: str


class UserAuthDetails(BaseModel):
    username: str
    roles: List[Role]
    permissions: List[Permission]


class Token(BaseModel):
    access_token: str
    token_type: str
