import json
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
            *,
            user_chat_repo: UserChatAssociationRepo,
            user_repo: UserRepo,
            chat_manager: ChatManager,
            message_repo: MessageRepo,
            current_user: Optional[tables.User]
    ):
        self._chat_repo = chat_repo
        self._user_chat_repo = user_chat_repo
        self._user_repo = user_repo
        self._chat_manager = chat_manager
        self._current_user = current_user
        self._message_repo = message_repo

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def get_unread_msg_count(self) -> int:
        pass

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def get_message_history(self, chat_id):
        pass

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def get_my_dialogs(self) -> list[views.DialogItem]:
        _ = await self._user_chat_repo.get_chats(self._current_user.id)
        dialogs = list()
        for companion, uca, chat in _:
            dialogs.append(
                views.DialogItem(
                    id=chat.id,
                    title=f"{companion.first_name} {companion.last_name} {companion.patronymic}",
                    job_title=companion.job_title,
                    departament=companion.department,
                    avatar_id=companion.avatar_id,
                    message_count=await self._message_repo.count(chat_id=chat.id),
                    unread_count=await self._message_repo.count(chat_id=chat.id, is_read=False),
                    role=companion.role
                )
            )
        return dialogs

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
            message_count=await self._message_repo.count(chat_id=chat_id),
            unread_count=await self._message_repo.count(chat_id=chat_id, is_read=False),
            role=companion.role
        )

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def subscribe_to_chat(self, websocket: WebSocket, chat_id: uuid.UUID) -> None:
        # if user in room into database access check
        chat_companions = await self._user_chat_repo.get_all(chat_id=chat_id)
        is_found = False
        for companion in chat_companions:
            if str(self._current_user.id) == str(companion.user_id):
                is_found = True

        if not is_found:
            raise AccessDenied("Для начала создайте диалог")

        await self._user_repo.session.close()

        if not self._chat_manager.is_exists(chat_id):
            await self._chat_manager.create_room(room_id=chat_id)
        await self._chat_manager.connect(websocket, room_id=chat_id)

        ws = self._chat_manager.get_room_ws(room_id=chat_id)
        while websocket.client_state == WebSocketState.CONNECTED:
            response = await ws.receive_text(websocket)

            try:
                input_data = schemas.MessageInput(**json.loads(response))
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

                if len(input_data.files) > 10:
                    raise BadRequest("Максимальное кол-во файлов - 10")

                files = list()
                for file_id in input_data.files:
                    file = await file_repo.get(id=file_id)
                    if not file:
                        continue  # todo raise

                    if file.message_id:
                        continue  # todo raise

                    await file_repo.update(file.id, message_id=message_id)
                    files.append(
                        schemas.MessageFileInclusion(
                            title=file.file_name,
                            file_id=str(file.id)
                        )
                    )
                owner = await self._user_repo.get(id=self._current_user.id)

            output_data = views.MessageOutput(
                id=str(message_id),
                text=input_data.text,
                avatar_id=str(owner.avatar_id) if owner.avatar_id else None,
                owner_id=str(owner.id),
                first_name=owner.first_name,
                last_name=owner.last_name,
                patronymic=owner.patronymic,
                files=files,
                is_read=message_obj.is_read,
                create_at=message_obj.create_at,
                update_at=message_obj.update_at
            )
            await self._chat_manager.send_data(chat_id, output_data.json())

        await self._chat_manager.disconnect(websocket, room_id=chat_id)
