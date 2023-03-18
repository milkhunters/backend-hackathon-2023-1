import uuid
from typing import Optional

from src.exceptions import AccessDenied, NotFound
from src.models import tables, schemas
from src.models.enums.role import UserRole
from src.models.schemas.user import is_valid_password
from src.services.auth import get_hashed_password, verify_password
from src.services.auth.utils import filters
from src.services.repository import UserRepo


class UserApplicationService:

    def __init__(self, user_repo: UserRepo, *, current_user: Optional[tables.User], debug: bool = False):
        self._repo = user_repo
        self._current_user = current_user
        self._debug = debug

    @filters(roles=[UserRole.ADMIN, UserRole.USER])
    async def get_me(self) -> schemas.User:
        return schemas.User.from_orm(await self._repo.get(id=self._current_user.id))

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def get_user(self, user_id: uuid.UUID) -> schemas.UserSmall | schemas.UserMiddle | schemas.User:
        user = await self._repo.get(id=user_id)

        if not user:
            raise NotFound(f"Пользователь с id {user_id!r} не найден!")

        if self._current_user.id == user_id:
            return schemas.User.from_orm(user)

        if self._current_user.role == UserRole.USER:
            return schemas.UserSmall.from_orm(user)

        if self._current_user.role == UserRole.HIGH_USER:
            return schemas.UserMiddle.from_orm(user)

        if self._current_user.role == UserRole.ADMIN:
            return schemas.User.from_orm(user)

    @filters(roles=[UserRole.ADMIN, UserRole.HIGH_USER, UserRole.USER])
    async def update_me(self, data: schemas.UserUpdate) -> None:
        await self._repo.update(
            id=self._current_user.id,
            **data.dict(exclude_unset=True)
        )

    @filters(roles=[UserRole.ADMIN])
    async def update_user(self, user_id: uuid.UUID, data: schemas.UserUpdateByAdmin) -> None:
        user = await self._repo.get(id=user_id)

        if not user:
            raise NotFound(f"Пользователь с id {user_id!r} не найден!")

        await self._repo.update(
            id=user_id,
            **data.dict(exclude_unset=True)
        )

    @filters(roles=[UserRole.ADMIN])
    async def delete_user(self, user_id: uuid.UUID) -> None:
        if self._current_user.id != uuid.UUID:
            await self._repo.delete(id=user_id)
        else:
            raise AccessDenied("Вы не можете удалить самого себя")

    @filters(roles=[UserRole.ADMIN, UserRole.USER, UserRole.HIGH_USER])
    async def user_password_update_by_user(self, new_password: schemas.UserPasswordUpdate):
        user = await self._repo.get(id=self._current_user.id)
        hashed_password = get_hashed_password(new_password.password)
        await self._repo.update(
            id=self._current_user.id,
            hashed_password=hashed_password
        )
