from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.repositories.user_repo import UserRepository
from app.models.user_model import UserCreate
from app.dependencies.auth import create_access_token
from datetime import timedelta
from jose import jwt, JWTError
from app.constants.token_constants import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth", tags=["Autenticación"])
user_repo = UserRepository()


@router.post("/register")
async def register(user: UserCreate):
    if await user_repo.get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    await user_repo.create_user(user.dict())
    return {"msg": "Usuario registrado"}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_repo.get_user_by_username(form_data.username)
    if not user or not user_repo.verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token(
        data={
            "sub": user["username"],
            "roles": user.get("roles", []),
            "permissions": user.get("permissions", []),
        }
    )
    return {"access_token": token, "token_type": "bearer"}


@router.post("/forgot-password")
async def forgot_password(username: str):
    user = user_repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    reset_token = create_access_token(
        data={"sub": username, "action": "password_reset"},
        expires_delta=timedelta(minutes=15),
    )

    return {"reset_token": reset_token}


@router.post("/reset-password")
async def reset_password(token: str, new_password: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        action: str = payload.get("action")

        if username is None or action != "password_reset":
            raise HTTPException(
                status_code=400, detail="Token inválido o tipo incorrecto"
            )

        user_repo.update_password(username, new_password)
        return {"msg": "Contraseña actualizada correctamente"}

    except JWTError:
        raise HTTPException(
            status_code=400, detail="El token ha expirado o es inválido"
        )
