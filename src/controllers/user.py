import uuid

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory

from src.views.user import UserSmallResponse, UserSmallListResponse
from src.views.user import UserBigResponse

router = APIRouter()


@router.get("/current", response_model=UserBigResponse, status_code=http_status.HTTP_200_OK)
async def get_current_user(services: ServiceFactory = Depends(get_services)):
    return UserBigResponse(message=await services.user.get_me())


@router.post("/update", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_user(data: schemas.UserUpdate, services: ServiceFactory = Depends(get_services)):
    await services.user.update_me(data)


@router.post("/update_password", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_my_password(data: schemas.UserPasswordUpdate, services: ServiceFactory = Depends(get_services)):
    await services.user.update_my_password(data)


@router.get("/list", response_model=UserSmallListResponse, status_code=http_status.HTTP_200_OK)
async def get_users(service: ServiceFactory = Depends(get_services)):
    return UserSmallListResponse(message=await service.user.get_users())


@router.get("/{user_id}", response_model=UserSmallResponse, status_code=http_status.HTTP_200_OK)
async def get_user(user_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    return UserSmallResponse(message=await services.user.get_user(user_id))
