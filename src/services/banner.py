import uuid
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.sql import roles

from src import views
from src.exceptions import NotFound, BadRequest
from src.models import tables, schemas
from src.models.enums import UserRole
from src.models.enums.content_type import ContentType
from src.services.auth import filters
from src.services.repository import ArticleRepo, FileRepo, BannerRepo
from src.services.storage.base import AbstractStorage, File


class BannerApplicationService:

    def __init__(self, banner_repo: BannerRepo, *, current_user: Optional[tables.User]):
        self._banner_repo = banner_repo
        self._current_user = current_user

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def get_banners(self) -> list[schemas.Banner]:
        banners = await self._banner_repo.get_all()
        return [schemas.Banner.from_orm(banner) for banner in banners]
