from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.repositories.user_repo import UserRepository
from app.models.user_model import UserCreate, User, UserResponse, UserUpdate
from app.dependencies.auth import create_access_token, get_current_user
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


@router.get("/me", response_model=UserResponse)
async def get_my_data(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me/update")
async def update_my_profile(
    update_data: UserUpdate, current_user: User = Depends(get_current_user)
):
    data_to_update = update_data.model_dump(exclude_unset=True)

    if not data_to_update:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")

    if "username" in data_to_update:
        new_username = data_to_update["username"]

        if new_username != current_user.username:
            if user_repo.get_user_by_username(new_username):
                raise HTTPException(
                    status_code=400,
                    detail="El nombre de usuario ya está en uso por otra persona",
                )

    sensitive_fields = {"username", "password"}
    requires_relogin = any(field in data_to_update for field in sensitive_fields)
    user_repo.update_user_data(current_user.username, data_to_update)

    if requires_relogin:
        return {
            "status": "requires_relogin",
            "message": "Credenciales actualizadas. Por seguridad, debe iniciar sesión nuevamente.",
        }

    return {"status": "success", "message": "Perfil actualizado correctamente"}


@router.delete("/me/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_account(current_user: User = Depends(get_current_user)):
    result = await user_repo.delete_user(current_user.username)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None
