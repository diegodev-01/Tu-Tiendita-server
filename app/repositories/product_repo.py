from bson import ObjectId
from typing import List


class ProductRepository:
    def __init__(self, db):
        self.collection = db["products"]

    async def create(self, product_data: dict) -> str:
        result = await self.collection.insert_one(product_data)
        return str(result.inserted_id)

    async def get_all(self) -> List[dict]:
        products = await self.collection.find().to_list(1000)
        for p in products:
            p["_id"] = str(p["_id"])
        return products

    async def update(self, product_id: str, update_data: dict) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(product_id)}, {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete_many(self, ids: List[str]) -> int:
        object_ids = [ObjectId(i) for i in ids]
        result = await self.collection.delete_many({"_id": {"$in": object_ids}})
        return result.deleted_count
