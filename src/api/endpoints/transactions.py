from fastapi import APIRouter, Depends
from db import db
from src.dependencies.auth import get_current_user
from src.schemas.auth_schema import UserAuthDetails
from src.schemas.transaction_schema import TransactionCreate
from src.services.transaction_service import TransactionService

router = APIRouter()

def get_transaction_service():
    return TransactionService(db)

@router.post("/", response_model=dict)
async def create_transaction(
    tx_in: TransactionCreate,
    current_user: UserAuthDetails = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service)
):
    tx_id = await service.create_transaction(tx_in, current_user.id)
    return {"message": "Venta registrada", "id": tx_id}

@router.get("/daily-summary", response_model=dict)
async def get_daily_summary(
    current_user: UserAuthDetails = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service)
):
    return await service.get_daily_summary(current_user.id)

@router.get("/top-products", response_model=list)
async def get_top_products(
    limit: int = 5,
    current_user: UserAuthDetails = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service)
):
    return await service.get_top_products(current_user.id, limit)

@router.get("/reports", response_model=dict)
async def get_reports(
    current_user: UserAuthDetails = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service)
):
    return await service.get_reports(current_user.id)

@router.get("/daily-details", response_model=list)
async def get_daily_details(
    current_user: UserAuthDetails = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service)
):
    return await service.get_daily_details(current_user.id)
