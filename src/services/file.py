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
from src.services.repository import ArticleRepo, FileRepo
from src.services.storage.base import AbstractStorage, File


class FileApplicationService:

    def __init__(self, file_repo: FileRepo, file_storage: AbstractStorage, *, current_user: Optional[tables.User]):
        self._file_storage = file_storage
        self._file_repo = file_repo  # TODO: схожие нейминги
        self._current_user = current_user

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def get_file_info(self, file_id: uuid.UUID) -> views.FileItem:
        file = await self._file_repo.get(id=file_id)
        if not file:
            NotFound(f"Файл с id {file_id!r} не найден")

        async with self._file_storage as storage:
            file_info = await storage.get(
                file_id=file_id,
                load_bytes=False
            )

        if not file_info:
            raise NotFound(f"Файл с id {file_id!r} удален с хранилища")

        return views.FileItem(
            id=file_id,
            title=file.file_name,
            content_type=file_info.content_type
        )

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def get_file(self, file_id: uuid.UUID):
        file = await self._file_repo.get(id=file_id)
        if not file:
            NotFound(f"Файл с id {file_id!r} не найден")

        async with self._file_storage as storage:
            file_info = await storage.get(
                file_id=file_id,
                load_bytes=True
            )

        if not file_info:
            raise NotFound(f"Файл с id {file_id!r} удален с хранилища")

        return file_info.bytes

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def save_file(self, file: UploadFile) -> views.FileItem:
        if not ContentType.has_value(file.content_type):
            raise BadRequest(f"Неизвестный тип файла {file.content_type!r}")

        # if len(file) > 20971520:
        #     pass

        # todo: filename null case

        file_id = await self._file_repo.create(
            file_name=file.filename
        )

        async with self._file_storage as storage:
            await storage.save(
                file_id=file_id,
                title=file.filename,
                content_type=file.content_type,
                file=await file.read(),
                owner_id=self._current_user.id
            )
        return views.FileItem(
            id=file_id,
            title=file.filename,
            content_type=file.content_type
        )
