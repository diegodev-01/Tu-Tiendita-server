from fastapi import FastAPI

from src.api.api import api_router

app = FastAPI(title="Tu Tiendita Server")

app.include_router(api_router, prefix="/api")
