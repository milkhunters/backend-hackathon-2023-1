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

