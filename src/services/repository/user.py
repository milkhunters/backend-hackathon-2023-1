from typing import Optional

from sqlalchemy import insert, update, delete, func, select

from src.models import tables
from src.services.repository.base import BaseRepository


class UserRepo(BaseRepository[tables.User]):
    table = tables.User

    async def get_by_username_insensitive(self, username: str) -> Optional[tables.User]:
        return (await self._conn.execute(
            select(self.table).where(func.lower(self.table.username) == username.lower())
        )).scalar_one_or_none()

    async def get_by_email_insensitive(self, email: str) -> Optional[tables.User]:
        return (await self._conn.execute(
            select(self.table).where(func.lower(self.table.email) == email.lower())
        )).scalar_one_or_none()
