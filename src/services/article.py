import uuid
from typing import Optional

from sqlalchemy.sql import roles

from src.exceptions import NotFound
from src.models import tables, schemas
from src.models.enums import UserRole
from src.services.auth import filters
from src.services.repository import ArticleRepo
from src.views import CreateArticleResponse


class ArticleApplicationService:


    def __init__(self, article_repo: ArticleRepo, current_user: Optional[tables.User], debug: bool = False):
        self._conn = None
        self.table = None
        self._repo = article_repo
        self._current_user = current_user
        self._debug = debug

    @filters(roles=[UserRole.ADMIN])
    async def get_article(self, article_id: uuid.UUID) -> schemas.Article:
        article = await self._repo.get(id=article_id)

        if not article:
            raise NotFound(f"Статья с id {article_id!r} не найдена!")

        return schemas.Article.from_orm(article)

    @filters(roles=[UserRole.ADMIN])
    async def get_article_list_range(self, count: int) -> list[schemas.Article]:
        return await self._repo.get_range(count)

    @filters(roles=[UserRole.ADMIN])
    async def create_article(self, article: schemas.Article):
        return await self._repo.create(**article.dict())

    @filters(roles=[UserRole.ADMIN])
    async def update_article(self, article_id: uuid.UUID, data: schemas.ArticleUpdate):
        article = await self._repo.get(id=article_id)

        if not article:
            raise NotFound(f"Статья с id {article_id!r} не найдена!")

        await self._repo.update(
            id=article_id,
            **data.dict(exclude_unset=True)
        )

    @filters(roles=[UserRole.ADMIN])
    async def delete_article(self, article_id: uuid.UUID):
        article = await self._repo.get(id=article_id)

        if not article:
            raise NotFound(f"Статья с id {article_id!r} не найдена!")

        await self._repo.delete(id=article_id)
