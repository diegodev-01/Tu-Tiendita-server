from fastapi import HTTPException
from bson import ObjectId
from src.models.user import UpdateUserDTO
# Ejemplo ficticio de hashing, usa tu método actual (ej. pwd_context.hash)
# from core.security import get_password_hash 

class UserService:
    def __init__(self, db):
        self.collection = db["users"]

    async def get_user_profile(self, user_id: str):
        user_doc = await self.collection.find_one({"_id": ObjectId(user_id)})
        if not user_doc:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        user_doc["_id"] = str(user_doc["_id"])
        return user_doc

    async def update_user_profile(self, user_id: str, update_data: UpdateUserDTO):
        # Convertimos a diccionario ignorando los campos que vengan como None
        update_dict = update_data.model_dump(exclude_none=True)
        
        if not update_dict:
            raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")
        
        # Si viene password, lo hasheamos antes de guardar en la DB
        if "password" in update_dict:
            # update_dict["password"] = get_password_hash(update_dict["password"])
            pass  # Descomenta la línea de arriba y usa tu función de hashing
        
        # Estructuramos el operador $set de MongoDB
        update_op = {"$set": update_dict}
        
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)}, 
            update_op
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
        return {"message": "Perfil actualizado correctamente"}