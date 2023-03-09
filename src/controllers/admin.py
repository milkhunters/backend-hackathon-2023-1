import uuid

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory

from src.views.user import UserBigResponse

router = APIRouter()


@router.get("/get_user/{user_id}", response_model=UserBigResponse, status_code=http_status.HTTP_200_OK)
async def get_user(user_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    return UserBigResponse(message=await services.admin.get_user(str(user_id)))


@router.post("/update_user/{user_id}", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_user(
        user_id: uuid.UUID,
        data: schemas.UserUpdateAdminMode,
        services: ServiceFactory = Depends(get_services)
):
    await services.admin.update_user(str(user_id), data)
