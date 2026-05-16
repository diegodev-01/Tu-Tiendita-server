from fastapi import APIRouter
from src.api.endpoints import products, auth, profile

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Autenticacion"])
api_router.include_router(products.router, prefix="/products", tags=["Productos"])
api_router.include_router(profile.router, prefix="/profile", tags=["Perfil"])
