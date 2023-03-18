import uuid
from typing import Optional

from sqlalchemy import insert, update, delete, func, select, or_, and_
from sqlalchemy.orm import joinedload, selectinload

from src.models import tables
from src.services.repository.base import BaseRepository


class UserChatAssociationRepo(BaseRepository[tables.UserChatAssociation]):
    table = tables.UserChatAssociation

    async def get_chat_id(self, user_id_one, user_id_two) -> Optional[uuid.UUID]:
        uca = self.table.__table__
        u = tables.User.__table__
        c = tables.Chat.__table__

        request = select(uca.c.chat_id) \
            .select_from(uca.join(u).join(c)) \
            .where(or_(uca.c.user_id == user_id_one, uca.c.user_id == user_id_two)) \
            .group_by(uca.c.chat_id) \
            .having(func.count(uca.c.user_id) == 2)

        result = await self._conn.execute(request)
        return result.scalar()

    async def get__info(self, user_id: uuid.UUID):
        # todo test
        request = select(tables.User, self.table, tables.Chat). \
            join(self.table, and_(tables.User.id == self.table.user_id)). \
            join(tables.Chat, and_(self.table.chat_id == tables.Chat.id)). \
            options(joinedload(tables.User.chats), selectinload(tables.Chat.users)). \
            where(and_(self.table.chat_id.in_(
            select(self.table.chat_id).filter_by(user_id=user_id)),
            tables.User.id != user_id))
