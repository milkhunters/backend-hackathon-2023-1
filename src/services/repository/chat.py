import uuid
from typing import Optional

from sqlalchemy import insert, update, delete, func, select
from sqlalchemy.orm import selectinload

from src.models import tables
from src.services.repository.base import BaseRepository


class ChatRepo(BaseRepository[tables.Chat]):
    table = tables.Chat

    async def get_chat_with_unread_count(self, user_id: uuid.UUID) -> list[tuple[tables.Chat, int]]:
        result = (
            select(tables.Chat, func.count(tables.Message.id))
            .join(tables.UserChatAssociation)
            .join(tables.Message)
            .where(tables.UserChatAssociation.user_id == user_id)
            .where(tables.Message.is_read == False)
            .where(tables.Message.owner_id != user_id)
            .group_by(tables.Chat.id)
        )
        return (await self.session.execute(result)).all()
