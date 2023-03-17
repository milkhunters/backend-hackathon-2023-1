import enum
import uuid

from pydantic import BaseModel, validator

from src.models.enums import UserRole


class Dialog(BaseModel):
    id: uuid.UUID
    name: str
    jobTitle: str
    avatar: str
    department: str
    role: UserRole

    class Config:
        orm_mode = True
