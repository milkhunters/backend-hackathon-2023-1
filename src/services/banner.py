import uuid
from datetime import datetime
from typing import Optional

from src.exceptions import BadRequest
from src.models import tables, schemas
from src.models.enums import UserRole
from src.models.schemas import Banner
from src.services.auth import filters
from src.services.repository import ArticleRepo, FileRepo, BannerRepo


class BannerApplicationService:

    def __init__(self, banner_repo: BannerRepo, file_repo: FileRepo, *, current_user: Optional[tables.User]):
        self._banner_repo = banner_repo
        self._current_user = current_user
        self._file_repo = file_repo

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def get_banners(self) -> list[schemas.Banner]:
        banners = await self._banner_repo.get_all()
        return [schemas.Banner.from_orm(banner) for banner in banners]

    @filters(roles=[UserRole.ADMIN])
    async def add_banner(self, file_id: uuid.UUID):
        file = await self._file_repo.get(id=file_id)
        if not file:
            raise BadRequest(f"Файл {file_id} не был обнаружен!")

        banner = Banner(file_id=file_id)
        await self._banner_repo.create(**banner.dict())

