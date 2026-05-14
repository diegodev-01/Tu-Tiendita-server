from pydantic import BaseModel, Field
from typing import List
from src.models.user import Role, Permission


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserAuthDetails(BaseModel):
    id: str = Field(alias=("sub"))
    name: str
    email: str
    roles: List[Role]
    permissions: List[Permission]


class Token(BaseModel):
    access_token: str
    token_type: str
