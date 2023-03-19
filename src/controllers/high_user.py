import uuid

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory

router = APIRouter()


@router.post("/update_user", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_user(
        user_id: uuid.UUID,
        data: schemas.UserUpdateByHigh,
        services: ServiceFactory = Depends(get_services)
):
    await services.user.update_user_byHigh(user_id, data)


@router.post("/update_user/password", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_user_password(
        user_id: uuid.UUID,
        password: str,
        service: ServiceFactory = Depends(get_services)
):
    await service.user.update_user_password(user_id, password)