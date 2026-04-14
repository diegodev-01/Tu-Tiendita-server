from fastapi import APIRouter, HTTPException, status
from app.models.product_model import ProductModel
from app.repositories.product_repo import ProductRepository
from db import db
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])
repo = ProductRepository(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel):
    product_id = await repo.create(product.dict())
    return {"message": "Producto creado.", "id": product_id}


@router.get("/")
async def get_products():
    return await repo.get_all()


@router.put("/{id}")
async def update_product(id: str, product_update: ProductModel):
    update_data = {k: v for k, v in product_update.dict().items() if v is not None}
    success = await repo.update(id, update_data)
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto actualizado."}


@router.delete("/")
async def delete_products(ids: List[str]):
    deleted_count = await repo.delete_many(ids)
    return {"message": f"Se eliminaron {deleted_count} productos."}
