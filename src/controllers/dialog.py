import uuid

from fastapi import APIRouter, Depends
from fastapi import status as http_status
from fastapi.websockets import WebSocket

from src.dependencies.services import get_services
from src.services import ServiceFactory
from src.views.dialog import DialogListResponse, DialogResponse
from src.views.message import MessageResponse, MessageCountResponse

router = APIRouter()


@router.get("/list", response_model=DialogListResponse, status_code=http_status.HTTP_200_OK)
async def get_dialog_list(services: ServiceFactory = Depends(get_services)):
    return DialogListResponse(message=await services.chat.get_my_dialogs())


@router.get("/open", response_model=DialogResponse, status_code=http_status.HTTP_200_OK)
async def open_dialog(user_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    return DialogResponse(message=await services.chat.get_dialog_by_user(user_id))


@router.get("/message/read", status_code=http_status.HTTP_204_NO_CONTENT)
async def open_dialog(message_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    await services.chat.mark_msg_as_read(message_id)


@router.get("/unread_count", response_model=MessageCountResponse, status_code=http_status.HTTP_200_OK)
async def chat_history(services: ServiceFactory = Depends(get_services)):
    return MessageCountResponse(message=await services.chat.get_unread_msg_count())


@router.get("/{dialog_id}/history", response_model=MessageResponse, status_code=http_status.HTTP_200_OK)
async def chat_history(dialog_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    return MessageResponse(message=await services.chat.get_message_history(dialog_id))


@router.websocket("/{dialog_id}/ws")
async def open_dialog(dialog_id: uuid.UUID, websocket: WebSocket, services: ServiceFactory = Depends(get_services)):
    await services.chat.subscribe_to_chat(websocket, dialog_id)
