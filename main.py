from fastapi import FastAPI
from db import db

app = FastAPI(title="Tu Tiendita Server")


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
