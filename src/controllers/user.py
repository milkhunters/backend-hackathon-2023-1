import uuid

from fastapi import APIRouter, Depends
from fastapi import status as http_status
from fastapi.requests import Request
from fastapi.responses import Response

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
    return UserSmallResponse(message=await services.user.get_user(str(user_id)))


@router.post("/update", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_user(data: schemas.UserUpdate, services: ServiceFactory = Depends(get_services)):
    await services.user.update_me(data)


@router.delete("/delete", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def delete_user(request: Request, response: Response, services: ServiceFactory = Depends(get_services)):
    await services.user.delete_me()
    await services.auth.logout(request, response)  # TODO: разлогин через Redis
