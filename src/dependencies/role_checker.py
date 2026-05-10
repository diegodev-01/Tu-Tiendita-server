from typing import List

from fastapi import Depends, HTTPException, status

from src.dependencies.auth import get_current_user
from src.models.role import Role
from src.schemas.auth_schema import UserAuthDetails


class RoleChecker:
    def __init__(self, allowed_roles: List[Role]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UserAuthDetails = Depends(get_current_user)):
        if not any(role in self.allowed_roles for role in user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes los roles necesarios para esta acción.",
            )
        return True
