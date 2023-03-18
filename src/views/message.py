import uuid
from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from src.models.schemas import MessageFileInclusion


class MessageOutput(BaseModel):
    id: uuid.UUID
    text: Optional[str]
    avatar_id: Optional[uuid.UUID]
    owner_id: uuid.UUID
    first_name: str
    last_name: str
    patronymic: Optional[str]
    is_read: bool
    files: list[MessageFileInclusion]

    create_at: datetime
    update_at: Optional[datetime]
