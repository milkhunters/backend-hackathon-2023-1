import uuid

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory

from src.views.user import UserBigResponse

router = APIRouter()


@router.delete("/delete_user", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    await services.user.delete_user(user_id)


@router.post("/update_user", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_user(
        user_id: uuid.UUID,
        data: schemas.UserUpdateByAdmin,
        services: ServiceFactory = Depends(get_services)
):
    await services.user.update_user(user_id, data)


@router.put("/create_user", status_code=http_status.HTTP_201_CREATED)
async def sign_up(user: schemas.UserSignUp, service: ServiceFactory = Depends(get_services)):
    await service.auth.create_user(user)
