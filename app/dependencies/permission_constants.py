from fastapi import Depends
from app.dependencies.auth import PermissionChecker
from app.models.permission_model import Permission

can_create_product = Depends(PermissionChecker(Permission.PRODUCT_CREATE))
can_edit_product = Depends(PermissionChecker(Permission.PRODUCT_EDIT))
can_delete_product = Depends(PermissionChecker(Permission.PRODUCT_DELETE))
can_view_product = Depends(PermissionChecker(Permission.PRODUCT_VIEW))
