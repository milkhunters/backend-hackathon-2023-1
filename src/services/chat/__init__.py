import uuid
from typing import Optional

from starlette.websockets import WebSocket, WebSocketState

from src import views
from src.exceptions import AccessDenied, NotFound
from src.models import tables, schemas
from src.models.enums.role import UserRole
from src.services.auth.utils import filters
from src.services.chat.utils import ChatManager
from src.services.repository import UserRepo


class ChatApplicationService:

    def __init__(self, chat_repo: UserRepo, _chat_manager: ChatManager, *, current_user: Optional[tables.User]):
        self._chat_repo = chat_repo
        self._chat_manager = _chat_manager
        self._current_user = current_user

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def get_dialogs(self) -> list[views.DialogResponse]:
        return schemas.User.from_orm(await self._repo.get(id=self._current_user.id))

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def subscribe_to_chat(self, websocket: WebSocket, chat_id: uuid.UUID) -> None:
        # if user in room into database access check

        if not self._chat_manager.is_exists(chat_id):
            await self._chat_manager.create_room(room_id=chat_id)
        await self._chat_manager.connect(websocket, room_id=chat_id)

        ws = self._chat_manager.get_room_ws(room_id=chat_id)
        while websocket.client_state == WebSocketState.CONNECTED:
            response = await ws.receive_text(websocket)
            await self._chat_manager.send_data(chat_id, "hello world")
            # save into database logic

        await self._chat_manager.disconnect(websocket, room_id=chat_id)

