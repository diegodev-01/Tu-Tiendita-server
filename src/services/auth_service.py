from typing import Optional
from passlib.context import CryptContext
from fastapi import HTTPException
from datetime import timedelta, datetime
from jose import jwt
from src.models.user import Role, Permission, User
from src.schemas.user_schema import UserResponse
from src.schemas.auth_schema import UserCreate
from src.constants.token_constants import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db):
        self.collection = db["users"]

    def verify_password(self, plain, hashed):
        return pwd_context.verify(plain, hashed)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def create_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    async def register_user(self, user_in: UserCreate):
        if await self.collection.find_one({"email": user_in.email}):
            raise HTTPException(status_code=400, detail="El usuario ya existe")

        new_user = User(
            name=user_in.name,
            email=user_in.email,
            password=self.get_password_hash(user_in.password),
            roles=[Role.CUSTOMER],
            permissions=[Permission.PRODUCT_VIEW],
        )
        user_dict = new_user.model_dump(by_alias=True)
        await self.collection.insert_one(user_dict)
        return {"msg": "Usuario registrado"}

    async def authenticate_user(self, email, password):
        user_doc = await self.collection.find_one({"email": email})
        if not user_doc:
            return None

        if not self.verify_password(password, user_doc["password"]):
            return None

        return UserResponse(**user_doc)
