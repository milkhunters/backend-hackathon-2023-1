import uuid

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory

from src.views.user import UserSmallResponse
from src.views.user import UserBigResponse

router = APIRouter()


@router.get("/current", response_model=UserBigResponse, status_code=http_status.HTTP_200_OK)
async def get_current_user(services: ServiceFactory = Depends(get_services)):
    return UserBigResponse(message=await services.user.get_me())


@router.get("/{user_id}", response_model=UserSmallResponse, status_code=http_status.HTTP_200_OK)
async def get_user(user_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    return UserSmallResponse(message=await services.user.get_user(user_id))


@router.post("/update", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_user(data: schemas.UserUpdate, services: ServiceFactory = Depends(get_services)):
    await services.user.update_me(data)


@router.put("/update_my_password", response_model=None, status_code=http_status.HTTP_200_OK)
async def update_user_password(data: schemas.UserPasswordUpdate, services: ServiceFactory = Depends(get_services)):
    await services.user.user_password_update_by_user(data)


@router.put("/update/avatar", response_model=None, status_code=http_status.HTTP_200_OK)
async def update_avatar(file_id: uuid.UUID, service: ServiceFactory = Depends(get_services)):
    pass