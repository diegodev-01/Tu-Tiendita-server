from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from jose import jwt, JWTError

from db import db
from src.schemas.auth_schema import UserCreate, Token
from src.services.auth_service import AuthService
from src.constants.token_constants import SECRET_KEY, ALGORITHM

router = APIRouter()


def get_auth_service():
    return AuthService(db)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate, service: AuthService = Depends(get_auth_service)
):
    return await service.register_user(user_in)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    user = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas"
        )

    token = service.create_token(
        data={
            "sub": user["username"],
            "roles": user.get("roles", []),
            "permissions": user.get("permissions", []),
        }
    )
    return {"access_token": token, "token_type": "bearer"}


@router.post("/forgot-password")
async def forgot_password(
    username: str, service: AuthService = Depends(get_auth_service)
):
    user = await service.collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    reset_token = service.create_token(
        data={"sub": username, "action": "password_reset"},
        expires_delta=timedelta(minutes=15),
    )
    return {"reset_token": reset_token}


@router.post("/reset-password")
async def reset_password(
    token: str, new_password: str, service: AuthService = Depends(get_auth_service)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        action: str = payload.get("action")

        if username is None or action != "password_reset":
            raise HTTPException(status_code=400, detail="Token inválido")

        hashed_password = service.get_password_hash(new_password)
        await service.collection.update_one(
            {"username": username}, {"$set": {"password": hashed_password}}
        )
        return {"msg": "Contraseña actualizada correctamente"}

    except JWTError:
        raise HTTPException(status_code=400, detail="Token expirado o inválido")
