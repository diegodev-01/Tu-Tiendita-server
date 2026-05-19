from datetime import datetime, timedelta, timezone
from bson import ObjectId
from fastapi import HTTPException
from src.schemas.transaction_schema import TransactionCreate

class TransactionService:
    def __init__(self, db):
        self.db = db
        self.collection = db["transactions"]

    async def get_store_id(self, user_id: str, provided_store_id: str = None) -> str:
        if provided_store_id:
            return provided_store_id
        store = await self.db["stores"].find_one({"ownerId": user_id})
        if not store:
            raise HTTPException(status_code=400, detail="El usuario no tiene una tienda")
        return str(store["_id"])

    async def create_transaction(self, tx_in: TransactionCreate, cashier_id: str) -> str:
        store_id = await self.get_store_id(cashier_id, tx_in.storeId)
        
        products_col = self.db["products"]
        cart_items = []
        total_amount = 0.0
        total_items = 0
        
        for item in tx_in.items:
            product = await products_col.find_one({"nfcTagId": item.nfcTagId, "storeId": store_id})
            if not product:
                raise HTTPException(status_code=404, detail=f"Producto con NFC {item.nfcTagId} no encontrado en tu tienda")
            
            if product.get("stock", 0) < item.quantity:
                raise HTTPException(status_code=400, detail=f"Stock insuficiente para {product.get('name')}")
            
            await products_col.update_one(
                {"_id": product["_id"]},
                {"$inc": {"stock": -item.quantity}}
            )
            
            price = product.get("price", 0.0)
            name = product.get("name", "Desconocido")
            
            cart_items.append({
                "productId": str(product["_id"]),
                "name": name,
                "price": price,
                "quantity": item.quantity
            })
            total_amount += price * item.quantity
            total_items += item.quantity
        
        tx_dict = {
            "storeId": store_id,
            "cashierId": cashier_id,
            "items": cart_items,
            "paymentMethod": tx_in.paymentMethod,
            "totalAmount": total_amount,
            "totalItems": total_items,
            "createdAt": datetime.now(timezone.utc),
            "type": "sale"
        }
        
        result = await self.collection.insert_one(tx_dict)
        return str(result.inserted_id)

    async def get_daily_summary(self, user_id: str):
        store_id = await self.get_store_id(user_id)
        
        now = datetime.now(timezone.utc)
        start_of_day = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
        
        pipeline = [
            {"$match": {"storeId": store_id, "type": "sale", "createdAt": {"$gte": start_of_day}}},
            {"$group": {
                "_id": None,
                "totalVentasMonto": {"$sum": "$totalAmount"},
                "numeroVentas": {"$sum": 1},
                "promedioPorVenta": {"$avg": "$totalAmount"}
            }}
        ]
        
        cursor = self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=1)
        
        if results:
            return {
                "totalVentasMonto": results[0]["totalVentasMonto"],
                "numeroVentas": results[0]["numeroVentas"],
                "promedioPorVenta": results[0]["promedioPorVenta"]
            }
        return {"totalVentasMonto": 0, "numeroVentas": 0, "promedioPorVenta": 0}

    async def get_top_products(self, user_id: str, limit: int = 5):
        store_id = await self.get_store_id(user_id)
        
        pipeline = [
            {"$match": {"storeId": store_id, "type": "sale"}},
            {"$unwind": "$items"},
            {"$group": {
                "_id": "$items.productId",
                "nombre": {"$first": "$items.name"},
                "cantidadVendida": {"$sum": "$items.quantity"}
            }},
            {"$sort": {"cantidadVendida": -1}},
            {"$limit": limit}
        ]
        
        cursor = self.collection.aggregate(pipeline)
        return await cursor.to_list(length=limit)

    async def get_reports(self, user_id: str):
        store_id = await self.get_store_id(user_id)
        now = datetime.now(timezone.utc)
        start_of_day = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
        start_of_week = start_of_day - timedelta(days=now.weekday())
        start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
        start_of_last_week = start_of_week - timedelta(days=7)
        end_of_last_week = start_of_week
        
        # We can do this with multiple queries or one complex aggregation. Multiple queries are easier to read.
        
        async def get_sum(start_date, end_date=None):
            match_query = {"storeId": store_id, "type": "sale", "createdAt": {"$gte": start_date}}
            if end_date:
                match_query["createdAt"]["$lt"] = end_date
            pipeline = [
                {"$match": match_query},
                {"$group": {"_id": None, "total": {"$sum": "$totalAmount"}, "count": {"$sum": 1}, "avg": {"$avg": "$totalAmount"}}}
            ]
            res = await self.collection.aggregate(pipeline).to_list(length=1)
            if res:
                return res[0]["total"], res[0]["count"], res[0]["avg"]
            return 0, 0, 0
            
        dia_total, _, dia_avg = await get_sum(start_of_day)
        sem_total, _, _ = await get_sum(start_of_week)
        mes_total, _, _ = await get_sum(start_of_month)
        last_sem_total, _, _ = await get_sum(start_of_last_week, end_of_last_week)
        
        # Overall average cart value
        _, _, overall_avg = await get_sum(datetime(2000, 1, 1, tzinfo=timezone.utc))
        
        return {
            "ventasDelDia": dia_total,
            "ventasSemanales": sem_total,
            "ventasMensuales": mes_total,
            "ventasSemanaPasada": last_sem_total,
            "comparacionSemanaPasada": sem_total - last_sem_total,
            "montoPromedioCarrito": overall_avg
        }

    async def get_daily_details(self, user_id: str):
        store_id = await self.get_store_id(user_id)
        now = datetime.now(timezone.utc)
        start_of_day = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
        
        cursor = self.collection.find({"storeId": store_id, "type": "sale", "createdAt": {"$gte": start_of_day}}).sort("createdAt", -1)
        transactions = await cursor.to_list(length=1000)
        
        details = []
        for tx in transactions:
            # We can join names if there are multiple, or just take the first one and say "+ X más"
            nombres = [item["name"] for item in tx.get("items", [])]
            nombre_display = ", ".join(nombres) if nombres else "Sin productos"
            
            details.append({
                "productos": nombre_display,
                "fechaHora": tx["createdAt"].isoformat(),
                "cantidadItems": tx.get("totalItems", 0),
                "metodoPago": tx.get("paymentMethod", "desconocido"),
                "montoTotal": tx.get("totalAmount", 0)
            })
            
        return details
