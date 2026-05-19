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
        existing_product = await self.collection.find_one({"name": product_in.name, "ownerId": ownerId})
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un producto con el nombre '{product_in.name}'",
            )
        
        store_id = product_in.storeId
        if not store_id:
            store = await self.collection.database["stores"].find_one({"ownerId": ownerId})
            if not store:
                raise HTTPException(status_code=400, detail="No se encontró una tienda para el usuario")
            store_id = str(store["_id"])
            
        product_dict = product_in.model_dump()
        product_dict["storeId"] = store_id

        product_data = Product(**product_dict, ownerId=ownerId)
        data_to_insert = product_data.model_dump(by_alias=True, exclude_none=True)
        result = await self.collection.insert_one(data_to_insert)
        return str(result.inserted_id)

    async def get_all_products(self, owner_id: str) -> List[dict]:
        cursor = self.collection.find({"ownerId": owner_id})
        products = await cursor.to_list(length=1000)
        return products

    async def update_product(self, product_id: str, product_in: ProductUpdate, owner_id: str) -> bool:
        update_data = product_in.model_dump(exclude_unset=True)
        if not update_data:
            return False

        update_data["updatedAt"] = datetime.now(timezone.utc)
        result = await self.collection.update_one(
            {"_id": ObjectId(product_id), "ownerId": owner_id}, {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete_many(self, ids: List[str], owner_id: str) -> int:
        object_ids = [ObjectId(i) for i in ids]
        result = await self.collection.delete_many({"_id": {"$in": object_ids}, "ownerId": owner_id})
        return result.deleted_count
