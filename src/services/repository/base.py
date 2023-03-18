import uuid
from typing import Generic, Type, TypeVar, Optional

from sqlalchemy import insert, update, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class BaseRepository(Generic[T]):
    table: Type[T]

    def __init__(self, conn: AsyncSession):
        self._conn = conn

    async def create(self, **kwargs) -> uuid.UUID:
        """
        Создает запись в БД

        :param kwargs:
        :return:
        """
        data = await self._conn.execute(insert(self.table).values(**kwargs))
        await self._conn.commit()
        return data.inserted_primary_key[0]  # todo: normalize it

    async def get(self, **kwargs) -> Optional[T]:
        """
        Получает запись

        :param kwargs:
        :return:
        """
        return (await self._conn.execute(select(self.table).filter_by(**kwargs))).scalars().first()

    async def get_all(self, **kwargs) -> list[Optional[T]]:
        """
        Получает все записи
        (лимит 100)

        :param kwargs:
        :return:
        """
        return (await self._conn.execute(select(self.table).filter_by(**kwargs).limit(100))).scalars().all()

    async def get_range(self, count: int, **kwargs):
        return (await self._conn.execute(select(self.table).filter_by(**kwargs).limit(count))).scalars().all()

    async def update(self, id: any, **kwargs) -> None:
        """
        Обновляет запись

        :param id:
        :param kwargs:
        :return:
        """
        if kwargs:
            await self._conn.execute(update(self.table).where(self.table.id == id).values(**kwargs))
            await self._conn.commit()

    async def delete(self, id: any) -> None:
        """
        Удаляет запись

        :param id:
        :return:
        """
        await self._conn.execute(delete(self.table).where(self.table.id == id))
        await self._conn.commit()

    async def count(self, **kwargs) -> int:
        """
        Возвращает количество записей

        :param kwargs:
        :return:
        """
        return (await self._conn.execute(select(func.count()).where(**kwargs))).scalar()

    @property
    def session(self):
        return self._conn
