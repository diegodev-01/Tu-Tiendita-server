from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from db import db
from src.schemas.store_schema import StoreResponse, StoreUpdate
from src.services.store_service import StoreService
from src.dependencies.auth import get_current_user
from src.schemas.auth_schema import UserAuthDetails

router = APIRouter()

def get_store_service():
    return StoreService(db)

@router.get("/", response_model=List[StoreResponse])
async def get_my_stores(
    current_user: UserAuthDetails = Depends(get_current_user),
    service: StoreService = Depends(get_store_service)
):
    return await service.get_stores_by_owner(current_user.id)

@router.get("/{store_id}", response_model=StoreResponse)
async def get_store_by_id(
    store_id: str,
    current_user: UserAuthDetails = Depends(get_current_user),
    service: StoreService = Depends(get_store_service)
):
    store = await service.get_store(store_id)
    if store["ownerId"] != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta tienda")
    return store

@router.put("/{store_id}", response_model=StoreResponse)
async def update_store(
    store_id: str,
    store_in: StoreUpdate,
    current_user: UserAuthDetails = Depends(get_current_user),
    service: StoreService = Depends(get_store_service)
):
    store = await service.get_store(store_id)
    if store["ownerId"] != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta tienda")
    
    return await service.update_store(store_id, store_in)

@router.delete("/{store_id}")
async def delete_store(
    store_id: str,
    current_user: UserAuthDetails = Depends(get_current_user),
    service: StoreService = Depends(get_store_service)
):
    store = await service.get_store(store_id)
    if store["ownerId"] != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta tienda")
    
    return await service.delete_store(store_id)
