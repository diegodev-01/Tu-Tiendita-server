from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.repositories.user_repo import UserRepository
from app.models.user_model import UserCreate
from app.dependencies.auth import create_access_token

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
    
    token = create_access_token(data={
        "sub": user["username"], 
        "roles": user.get("roles", []),
        "permissions": user.get("permissions", [])
    })
    return {"access_token": token, "token_type": "bearer"}