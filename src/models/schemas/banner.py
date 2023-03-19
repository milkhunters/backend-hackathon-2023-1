import uuid
from datetime import datetime
from typing import Any

from src.models.enums.error import ErrorType
from pydantic import BaseModel


class Banner(BaseModel):
    id: uuid.UUID
    file_id: uuid.UUID
    create_at: datetime

    class Config:
        orm_mode = True
