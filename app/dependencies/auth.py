from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.user_model import User, Role
from app.models.permission_model import Permission
from typing import List, Optional
from app.constants.token_constants import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        roles: List[Role] = payload.get("roles", [])
        permissions: List[Permission] = payload.get("permissions", [])
        
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
            
        return User(username=username, roles=roles, permissions=permissions)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No se pudo validar el token")

class RoleChecker:
    def __init__(self, allowed_roles: List[Role]):
        self.allowed_roles = allowed_roles
    def __call__(self, user: User = Depends(get_current_user)):
        for role in user.roles:
            if role in self.allowed_roles: return True
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos suficientes.")

class PermissionChecker:
    def __init__(self, required_permission: Permission):
        self.required_permission = required_permission
    def __call__(self, user: User = Depends(get_current_user)):
        if self.required_permission not in user.permissions:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado por falta de permisos.")
        return True