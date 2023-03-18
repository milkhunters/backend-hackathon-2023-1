import uuid
from typing import Optional

from pydantic import BaseModel

from src.models.enums import UserRole
from src.views.base import BaseView


class DialogItem(BaseModel):
    id: uuid.UUID
    title: str
    job_title: str
    departament: str
    avatar_id: Optional[str]
    role: UserRole


class DialogResponse(BaseView):
    message: DialogItem


class DialogListResponse(BaseView):
    message: list[DialogItem]
