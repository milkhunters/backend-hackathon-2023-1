import uuid
from typing import Optional

from fastapi.websockets import WebSocket, WebSocketState

from src import views
from src.dependencies.repos import get_repos
from src.exceptions import AccessDenied, NotFound, BadRequest
from src.models import tables, schemas
from src.models.enums.role import UserRole
from src.models.schemas import MessageInput
from src.services.auth.utils import filters
from src.services.chat.utils import ChatManager
from src.services.repository import ChatRepo, UserRepo, MessageRepo, FileRepo
from src.services.repository.user_chat import UserChatAssociationRepo


class ChatApplicationService:

    def __init__(
            self,
            chat_repo: ChatRepo,
            user_chat_repo: UserChatAssociationRepo,
            user_repo: UserRepo,
            chat_manager: ChatManager,
            *,
            current_user: Optional[tables.User]
    ):
        self._chat_repo = chat_repo
        self._user_chat_repo = user_chat_repo
        self._user_repo = user_repo
        self._chat_manager = chat_manager
        self._current_user = current_user

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def get_dialogs(self) -> list[views.DialogResponse]:
        pass

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def get_dialog_by_user(self, user_id: uuid.UUID) -> views.DialogItem:
        # todo user_id = current_id case
        companion = await self._user_repo.get(id=user_id)
        if not companion:
            raise NotFound(f"Пользователь {user_id!r} не найден")

        chat_id = await self._user_chat_repo.get_chat_id(
            user_id_one=self._current_user.id,
            user_id_two=companion.id
        )

        if not chat_id:
            chat_id = await self._chat_repo.create()
            for _id in [companion.id, self._current_user.id]:
                await self._user_chat_repo.create(
                    user_id=_id,
                    chat_id=chat_id
                )

        return views.DialogItem(
            id=chat_id,
            title=f"{companion.first_name} {companion.last_name} {companion.patronymic}",
            job_title=companion.job_title,
            departament=companion.department,
            avatar_id=companion.avatar_id,
            role=companion.role
        )

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def subscribe_to_chat(self, websocket: WebSocket, chat_id: uuid.UUID) -> None:
        # if user in room into database access check
        chat_companions = await self._user_chat_repo.get_all(chat_id=chat_id)
        is_found = False
        for companion in chat_companions:
            if self._current_user.id == companion.user_id:
                is_found = True

        if not is_found:
            raise AccessDenied("Для начала создайте диалог")

        await self._user_repo.session.close()

        if not self._chat_manager.is_exists(chat_id):
            await self._chat_manager.create_room(room_id=chat_id)
        await self._chat_manager.connect(websocket, room_id=chat_id)

        ws = self._chat_manager.get_room_ws(room_id=chat_id)
        while websocket.client_state == WebSocketState.CONNECTED:
            response = await ws.receive_json(websocket)

            try:
                input_data = schemas.MessageInput(**response)
            except ValueError:
                raise BadRequest("Словарь должен соответствовать принимаемой модели")

            # save into database logic
            scope = websocket.app.state
            async with scope.db_session() as session:
                message_repo = MessageRepo(session)
                message_id = await message_repo.create(
                    text=input_data.text,
                    chat_id=chat_id,
                    owner_id=self._current_user.id
                )
                message_obj = await message_repo.get(id=message_id)
                file_repo = FileRepo(session)
                for file in input_data.files:
                    # todo: check if in database
                    await file_repo.create(
                        file_name=file.title,
                        file_id=file.file_id,
                        message_id=message_id
                    )

            output_data = views.MessageOutput(
                id=message_id,
                text=input_data.text,
                avatar_id=self._current_user.avatar_id,
                owner_id=self._current_user.id,
                first_name=self._current_user.first_name,
                last_name=self._current_user.last_name,
                patronymic=self._current_user.patronymic,
                files=input_data.files,
                create_at=message_obj.create_at,
                update_at=message_obj.update_at
            )
            await self._chat_manager.send_data(chat_id, output_data.dict())

        await self._chat_manager.disconnect(websocket, room_id=chat_id)
