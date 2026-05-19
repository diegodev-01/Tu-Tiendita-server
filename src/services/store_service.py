from fastapi import HTTPException
from bson import ObjectId
from src.models.store import Store
from src.schemas.store_schema import StoreCreate, StoreUpdate

class StoreService:
    def __init__(self, db):
        self.db = db
        self.collection = db["stores"]

    async def get_store(self, store_id: str):
        store_doc = await self.collection.find_one({"_id": ObjectId(store_id)})
        if not store_doc:
            raise HTTPException(status_code=404, detail="Tienda no encontrada")
        store_doc["_id"] = str(store_doc["_id"])
        return store_doc

    async def get_stores_by_owner(self, owner_id: str):
        cursor = self.collection.find({"ownerId": owner_id})
        stores = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            stores.append(doc)
        return stores

    async def update_store(self, store_id: str, store_in: StoreUpdate):
        update_data = {k: v for k, v in store_in.model_dump().items() if v is not None}
        if update_data:
            result = await self.collection.update_one(
                {"_id": ObjectId(store_id)}, {"$set": update_data}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Tienda no encontrada")
        return await self.get_store(store_id)

    async def delete_store(self, store_id: str):
        result = await self.collection.delete_one({"_id": ObjectId(store_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Tienda no encontrada")
        return {"msg": "Tienda eliminada"}
