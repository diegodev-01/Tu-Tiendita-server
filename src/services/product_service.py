from bson import ObjectId
from typing import List
from src.schemas.product_schema import ProductCreate, ProductUpdate
from datetime import datetime


class ProductService:
    def __init__(self, db):
        self.collection = db["products"]

    async def create_product(self, product_in: ProductCreate) -> str:
        product_dict = product_in.model_dump()
        product_dict["sync_date"] = datetime.utcnow()
        result = await self.collection.insert_one(product_dict)
        return str(result.inserted_id)

    async def get_all_products(self) -> List[dict]:
        products = await self.collection.find().to_list(1000)
        for p in products:
            p["id"] = str(p.pop("_id"))
        return products

    async def update_product(self, product_id: str, product_in: ProductUpdate) -> bool:
        update_data = product_in.model_dump(exclude_unset=True)
        if not update_data:
            return False

        result = await self.collection.update_one(
            {"_id": ObjectId(product_id)}, {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete_multiple_products(self, ids: List[str]) -> int:
        object_ids = [ObjectId(i) for i in ids]
        result = await self.collection.delete_many({"_id": {"$in": object_ids}})
        return result.deleted_count
