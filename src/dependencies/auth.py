from typing import List
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.schemas.auth_schema import UserAuthDetails
from src.constants.token_constants import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserAuthDetails:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload["sub"]
        if email is None:
            raise credentials_exception

        name: str = payload["name"]
        roles: List[str] = payload["roles"]
        permissions: List[str] = payload["permissions"]

        return UserAuthDetails(
            name=name, email=email, roles=roles, permissions=permissions
        )
    except JWTError:
        raise credentials_exception
