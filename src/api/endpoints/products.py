from fastapi import APIRouter, Depends, HTTPException
from typing import List
from db import db
from src.dependencies.auth import get_current_user
from src.services.product_service import ProductService
from src.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from src.schemas.auth_schema import UserAuthDetails
from src.constants.permission_constants import (
    can_create_product,
    can_view_product,
    can_edit_product,
    can_delete_product,
)

router = APIRouter()


def get_product_service():
    return ProductService(db)


@router.post(
    "/",
    dependencies=[can_create_product],
    response_model=dict,
)
async def create(
    product_in: ProductCreate,
    current_user: UserAuthDetails = Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
):
    product_id = await service.create_product(product_in, ownerId=current_user.id)
    return {"message": "Producto creado", "id": product_id}


@router.get(
    "/",
    dependencies=[can_view_product],
    response_model=List[ProductResponse],
)
async def list_products(service: ProductService = Depends(get_product_service)):
    return await service.get_all_products()


@router.put("/{id}", dependencies=[can_edit_product])
async def update(
    id: str,
    product_in: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    success = await service.update_product(id, product_in)
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto actualizado"}


@router.delete("/", dependencies=[can_delete_product])
async def delete(
    ids: List[str], service: ProductService = Depends(get_product_service)
):
    count = await service.delete_many(ids)
    return {"message": f"Se eliminaron {count} productos"}
