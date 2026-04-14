from fastapi import APIRouter
from app.models.product_model import ProductModel

router = APIRouter()

@router.post("/products")
async def create_product(product: ProductModel):
    return {
        "message": "Producto creado correctamente",
        "data": product
    }