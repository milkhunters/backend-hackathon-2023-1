from src.models import tables
from src.services.repository.base import BaseRepository


class ArticleRepo(BaseRepository[tables.Article]):
    tables = tables.Article

    async def get_range(self, count: int):
        query = self.tables.select().limit(count)
        result = await self._conn.execute(query)
        return result.fetchall()
