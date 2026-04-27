from fastapi import HTTPException, Depends, status
from app.models.user_model import User, Role
from app.models.permission_model import Permission
from typing import List


def get_current_user() -> User:
    return User(
        username="fake_admin",
        roles=[Role.ADMIN],
        permissions=[
            Permission.PRODUCT_CREATE,
            Permission.PRODUCT_DELETE,
            Permission.PRODUCT_VIEW,
        ],
    )


class RoleChecker:
    def __init__(self, allowed_roles: List[Role]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        for role in user.roles:
            if role in self.allowed_roles:
                return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes los permisos necesarios para esta sección.",
        )


class PermissionChecker:
    def __init__(self, required_permission: Permission):
        self.required_permission = required_permission

    def __call__(self, user: User = Depends(get_current_user)):
        if self.required_permission not in user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No cuenta con los permisos necesarios.",
            )
        return True
