from fastapi import Depends
from src.models.permission import Permission
from src.dependencies.permission_checker import PermissionChecker

can_create_product = Depends(PermissionChecker(Permission.PRODUCT_CREATE))
can_edit_product = Depends(PermissionChecker(Permission.PRODUCT_EDIT))
can_delete_product = Depends(PermissionChecker(Permission.PRODUCT_DELETE))
can_view_product = Depends(PermissionChecker(Permission.PRODUCT_VIEW))
