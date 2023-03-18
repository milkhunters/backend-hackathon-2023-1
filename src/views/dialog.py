import uuid

from pydantic import BaseModel

from src.models.enums import UserRole
from src.views.base import BaseView


class DialogResponse(BaseModel):
    id: uuid.UUID
    title: str
    job_title: str
    departament: str
    avatar_id: str
    role: UserRole


class DialogListResponse(BaseView):
    message: list[DialogResponse]
