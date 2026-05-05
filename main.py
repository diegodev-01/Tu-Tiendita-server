from fastapi import FastAPI
from db import db
from app.routes.product_routes import router as product_router
from app.routes.auth_routes import router as auth_router

app = FastAPI(title="Tu Tiendita Server")
app.include_router(product_router)
app.include_router(auth_router)


@app.get("/")
async def read_root():
    return {"message": "Servidor funcionando"}


@app.get("/test-db")
async def test_db():
    coleccion = db["productos"]
    resultado = await coleccion.insert_one({"nombre": "Producto prueba", "precio": 10})

    return {
        "message": "Conexión exitosa a MongoDB",
        "inserted_id": str(resultado.inserted_id),
    }
