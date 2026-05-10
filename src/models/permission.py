from enum import Enum


class Permission(str, Enum):
    PRODUCT_CREATE = "product:create"
    PRODUCT_EDIT = "product:edit"
    PRODUCT_DELETE = "product:delete"
    PRODUCT_VIEW = "product:view"
