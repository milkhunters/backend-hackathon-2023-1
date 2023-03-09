import uuid
from typing import Optional

from src.exceptions import AccessDenied, NotFound
from src.models import tables, schemas
from src.models.enums.role import UserRole
from src.services.auth.utils import filters
from src.services.repository import UserRepo


class AdminApplicationService:

    def __init__(self, user_repo: UserRepo, *, current_user: Optional[tables.User], debug: bool = False):
        self._repo = user_repo
        self._current_user = current_user
        self._debug = debug

    @filters(roles=[UserRole.ADMIN])
    async def get_user(self, user_id: str) -> schemas.User:
        user = await self._repo.get(id=user_id)

        if not user:
            raise NotFound(f"User with id {user_id!r} not found")

        return schemas.User.from_orm(user)

    @filters(roles=[UserRole.ADMIN])
    async def update_user(self, user_id: str, data: schemas.UserUpdateAdminMode) -> None:
        await self._repo.update(
            id=user_id,
            **data.dict(exclude_unset=True)
        )
