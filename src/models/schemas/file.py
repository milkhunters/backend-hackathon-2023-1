import uuid

from pydantic import BaseModel


class File(BaseModel):
    id: uuid.UUID
    file_name: str
    file_id: uuid.UUID
    message_id: uuid.UUID

    class Config:
        orm_mode = True
