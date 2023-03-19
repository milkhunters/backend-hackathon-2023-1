import uuid
from typing import Optional

from sqlalchemy import insert, update, delete, func, select, and_
from sqlalchemy.orm import selectinload, subqueryload, joinedload, contains_eager

from src.models import tables
from src.services.repository.base import BaseRepository


class MessageRepo(BaseRepository[tables.Message]):
    table = tables.Message

    async def get_all(self, **kwargs) -> list[tables.Message]:
        return (
            await self._conn.execute(
                select(self.table).filter_by(**kwargs).limit(100)
                .options(contains_eager(tables.Message.owner), contains_eager(tables.Message.files))
            )
        ).unique().scalars().all()

    async def get_unread_by_user_id(self, user_id: uuid.UUID) -> int:
        result = (await self.session.execute(
            select(
                func.count(self.table.id)
            )
            .join(tables.Chat, tables.Chat.id == tables.Message.chat_id)
            .join(tables.UserChatAssociation, tables.UserChatAssociation.chat_id == tables.Chat.id)
            .where(and_(tables.UserChatAssociation.user_id == user_id, tables.Message.is_read == False, tables.Message.owner_id != user_id))
        )).scalar()
        return result
