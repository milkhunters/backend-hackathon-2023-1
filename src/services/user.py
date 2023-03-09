import uuid
from typing import Optional

from src.exceptions import AccessDenied, NotFound
from src.models import tables, schemas
from src.models.enums.role import UserRole
from src.services.auth.utils import filters
from src.services.repository import UserRepo


class UserApplicationService:

    def __init__(self, user_repo: UserRepo, *, current_user: Optional[tables.User], debug: bool = False):
        self._repo = user_repo
        self._current_user = current_user
        self._debug = debug

    @filters(roles=[UserRole.ADMIN, UserRole.USER])
    async def get_me(self) -> schemas.User:
        """
        Get UserBigResponse
        """
        return schemas.User.from_orm(await self._repo.get(id=self._current_user.id))

    @filters(roles=[UserRole.ADMIN, UserRole.USER])
    async def get_user(self, user_id: str) -> schemas.UserSmall:
        """
        Get user by id # todo: by all fields
        """
        user = await self._repo.get(id=user_id)

        if not user:
            raise NotFound(f"User with id {user_id!r} not found")

        return schemas.UserSmall.from_orm(user)

    @filters(roles=[UserRole.ADMIN, UserRole.USER])
    async def update_me(self, data: schemas.UserUpdate) -> None:
        await self._repo.update(
            id=self._current_user.id,
            **data.dict(exclude_unset=True)
        )

    @filters(roles=[UserRole.ADMIN, UserRole.USER])
    async def delete_me(self) -> None:
        await self._repo.delete(id=self._current_user.id)
