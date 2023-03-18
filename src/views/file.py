import uuid
from typing import Optional, Any

from pydantic import BaseModel

from src.models.enums import UserRole
from src.models.enums.content_type import ContentType
from src.views.base import BaseView


class FileItem(BaseModel):
    id: uuid.UUID
    title: str
    content_type: str


class FileResponse(BaseView):
    message: FileItem
