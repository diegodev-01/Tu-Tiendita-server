import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("Falta la variable de entorno MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)
db = client["tiendita_db"]