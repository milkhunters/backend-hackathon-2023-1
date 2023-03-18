import uuid

from pydantic import BaseModel


class UserUpdatePasswordByAdmin(BaseModel):
    id: uuid.UUID
    password: str
