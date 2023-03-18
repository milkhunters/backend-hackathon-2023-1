import uuid
import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

from src.models.enums.role import UserRole
from src.models.schemas.user import UserSmall
from src.models.schemas.file import File


class Message(BaseModel):
    id: uuid.UUID
    text: Optional[str]
    files: list[File]
    chat_id: uuid.UUID
    owner: list[UserSmall]
    is_read: bool

    create_at: datetime
    update_at: Optional[datetime]

    class Config:
        orm_mode = True


class MessageFileInclusion(BaseModel):
    title: str
    file_id: uuid.UUID


class MessageInput(BaseModel):
    text: Optional[str]
    files: list[uuid.UUID]
