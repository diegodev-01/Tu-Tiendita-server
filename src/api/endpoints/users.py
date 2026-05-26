from fastapi import APIRouter, Depends
from db import db
from src.dependencies.auth import get_current_user
from src.schemas.auth_schema import UserAuthDetails
from src.schemas.user_schema import UserProfileResponse
from src.services.user_service import UserService
from src.models.user import UpdateUserDTO

router = APIRouter()


def get_user_service():
    return UserService(db)


@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(
    current_user: UserAuthDetails = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return await service.get_user_profile(current_user.id)


@router.patch("/profile")
async def update_profile(
    body: UpdateUserDTO,
    current_user: UserAuthDetails = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return await service.update_user_profile(current_user.id, body)
