from fastapi import APIRouter, Depends

from db import db
from src.dependencies.auth import get_current_user
from src.schemas.auth_schema import UserAuthDetails
from src.schemas.user_schema import UserDataResponse, UserDataUpdate
from src.services.profile_service import ProfileService

router = APIRouter()


def get_user_service():
    return ProfileService(db)


@router.get("/", response_model=UserDataResponse)
async def get_my_data(
    service: ProfileService = Depends(get_user_service),
    current_user: UserAuthDetails = Depends(get_current_user),
):
    return await service.get_user_data(current_user.id)


@router.put("/")
async def update_my_profile(
    update_data: UserDataUpdate,
    service: ProfileService = Depends(get_user_service),
    current_user: UserAuthDetails = Depends(get_current_user),
):
    return await service.set_user_data(current_user.id, update_data)
