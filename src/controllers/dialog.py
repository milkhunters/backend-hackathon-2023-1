import uuid

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory
from src.views import dialog
from src.views.dialog import DialogListResponse, DialogResponse

router = APIRouter()


@router.get("/list", response_model=DialogListResponse, status_code=http_status.HTTP_200_OK)
async def get_dialog_list(services: ServiceFactory = Depends(get_services)):
    return DialogListResponse(message=await services.chat.get_my_dialogs())


@router.get("/open", response_model=DialogResponse, status_code=http_status.HTTP_200_OK)
async def open_dialog(user_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    return DialogResponse(message=await services.chat.get_dialog_by_user(user_id))
