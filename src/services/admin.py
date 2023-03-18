import uuid
from typing import Optional

from src.exceptions import AccessDenied, NotFound
from src.models import tables, schemas
from src.models.enums.role import UserRole
from src.models.schemas.user import is_valid_password
from src.services.auth import verify_password, get_hashed_password
from src.services.auth.utils import filters
from src.services.repository import UserRepo


class AdminApplicationService:

    def __init__(self, user_repo: UserRepo, *, current_user: Optional[tables.User], debug: bool = False):
        self._repo = user_repo
        self._current_user = current_user
        self._debug = debug

    @filters(roles=[UserRole.ADMIN])
    async def user_password_update_by_admin(self, data: schemas.UserUpdatePasswordByAdmin):
        user = await self._repo.get(id=data.id)
        if not user:
            raise NotFound(f"Пользователь с id {user.id!r} не найден!")

        if verify_password(data.password, storage=user.hashed_password):
            raise ValueError("Новый и старый пароль совпадают!")

        if not (is_valid_password(data.password)):
            raise ValueError("Слабый или невалидный password!")

        hashed_password = get_hashed_password(data.password)

        await self._repo.update(
            id=user.id,
            hashed_password=hashed_password
        )
