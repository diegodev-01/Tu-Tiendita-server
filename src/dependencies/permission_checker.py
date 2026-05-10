from fastapi import Depends, HTTPException, status

from src.dependencies.auth import get_current_user
from src.models.permission import Permission
from src.schemas.auth_schema import UserAuthDetails


class PermissionChecker:
    def __init__(self, required_permission: Permission):
        self.required_permission = required_permission

    def __call__(self, user: UserAuthDetails = Depends(get_current_user)):
        if self.required_permission not in user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes los permisos necesarios para esta accion",
            )
        return True
