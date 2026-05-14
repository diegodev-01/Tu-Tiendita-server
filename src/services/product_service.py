from datetime import datetime, timezone
from bson import ObjectId
from typing import List
from fastapi import HTTPException, status
from src.models.product import Product
from src.schemas.product_schema import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db):
        self.collection = db["products"]

    async def create_product(self, product_in: ProductCreate, ownerId: str) -> str:
        existing_product = await self.collection.find_one({"name": product_in.name})
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un producto con el nombre '{product_in.name}'",
            )
        product_data = Product(**product_in.model_dump(), ownerId=ownerId)
        data_to_insert = product_data.model_dump(by_alias=True, exclude_none=True)
        result = await self.collection.insert_one(data_to_insert)
        return str(result.inserted_id)

    async def get_all_products(self) -> List[dict]:
        cursor = self.collection.find()
        products = await cursor.to_list(length=1000)
        return products

    async def update_product(self, product_id: str, product_in: ProductUpdate) -> bool:
        update_data = product_in.model_dump(exclude_unset=True)
        if not update_data:
            return False

        update_data["updatedAt"] = datetime.now(timezone.utc)
        result = await self.collection.update_one(
            {"_id": ObjectId(product_id)}, {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete_many(self, ids: List[str]) -> int:
        object_ids = [ObjectId(i) for i in ids]
        result = await self.collection.delete_many({"_id": {"$in": object_ids}})
        return result.deleted_count
