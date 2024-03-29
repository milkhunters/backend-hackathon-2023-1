import uuid
from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from src.models.schemas import MessageFileInclusion
from src.views import BaseView


class MessageOutput(BaseModel):
    id: str
    text: Optional[str]
    avatar_id: Optional[str]
    owner_id: str
    first_name: str
    last_name: str
    patronymic: Optional[str]
    is_read: bool
    files: list[MessageFileInclusion]

    create_at: datetime
    update_at: Optional[datetime]


class MessageResponse(BaseView):
    message: list[MessageOutput]


class MessageCountResponse(BaseView):
    message: int
