from bson import ObjectId
from fastapi import HTTPException, status
from src.schemas.user_schema import UserDataResponse, UserDataUpdate


class ProfileService:
    def __init__(self, db):
        self.collection = db["users"]

    async def get_user_data(self, userId: str):
        try:
            userId = ObjectId(userId)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID de usuario proporcionado no es válido",
            )

        user = await self.collection.find_one({"_id": userId})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se encontro informacion sobre este usuario",
            )
        user_data = UserDataResponse(**user)
        return user_data

    async def set_user_data(self, userId: str, userData: UserDataUpdate):
        try:
            userId = ObjectId(userId)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID de usuario proporcionado no es válido",
            )
        update_data = userData.model_dump()
        result = await self.collection.update_one({"_id": userId}, {"$set": update_data})

        if not result.modified_count > 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"message": "Perfil Actualizado"}
